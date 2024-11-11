"""
Main entry point for the uripoint.
"""
# !/usr/bin/env python3
import argparse
import json
import sys
import asyncio
import uvicorn
from fastapi import FastAPI
from typing import Dict, Any, Optional
import os
from enum import Enum
import yaml
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
from aiortsp.server import RTSPServer
import socket
import threading
import paramiko
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import aiomqtt
import websockets
import smtplib
import poplib
from email.mime.text import MIMEText


class ProtocolType(str, Enum):
    HTTP = "http"
    FTP = "ftp"
    RTSP = "rtsp"
    MQTT = "mqtt"
    WEBSOCKET = "ws"
    TCP = "tcp"
    UDP = "udp"
    SMTP = "smtp"
    POP3 = "pop3"
    SFTP = "sftp"


class EndpointConfig:
    def __init__(self, uri: str, protocol: ProtocolType, port: int, handler_data: Dict[str, Any]):
        self.uri = uri
        self.protocol = protocol
        self.port = port
        self.handler_data = handler_data


class MultiProtocolServer:
    def __init__(self):
        self.endpoints: Dict[str, EndpointConfig] = {}
        self.config_file = "uripoint_config.yaml"
        self.http_app = FastAPI(title="URIPoint Multi-Protocol Server")
        self.servers = {}

    async def start_ftp_server(self, port: int, directory: str):
        authorizer = DummyAuthorizer()
        authorizer.add_anonymous(directory, perm="elradfmw")

        handler = FTPHandler
        handler.authorizer = authorizer

        server = FTPServer(("0.0.0.0", port), handler)
        threading.Thread(target=server.serve_forever).start()
        return server

    async def start_rtsp_server(self, port: int):
        server = RTSPServer()
        await server.start(port=port)
        return server

    async def start_mqtt_broker(self, port: int):
        config = {
            'listeners': {
                'default': {
                    'type': 'tcp',
                    'bind': f'0.0.0.0:{port}'
                }
            }
        }
        broker = aiomqtt.Broker(config)
        await broker.start()
        return broker

    async def start_websocket_server(self, port: int, handler_data: Dict):
        async def handler(websocket, path):
            await websocket.send(json.dumps(handler_data))

        server = await websockets.serve(handler, "0.0.0.0", port)
        return server

    def start_tcp_server(self, port: int, handler_data: Dict):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", port))
        sock.listen(5)

        def handle_client(client_socket):
            client_socket.send(json.dumps(handler_data).encode())
            client_socket.close()

        def server_loop():
            while True:
                client, addr = sock.accept()
                client_handler = threading.Thread(target=handle_client, args=(client,))
                client_handler.start()

        server_thread = threading.Thread(target=server_loop)
        server_thread.daemon = True
        server_thread.start()
        return sock

    def start_udp_server(self, port: int, handler_data: Dict):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", port))

        def server_loop():
            while True:
                data, addr = sock.recvfrom(1024)
                sock.sendto(json.dumps(handler_data).encode(), addr)

        server_thread = threading.Thread(target=server_loop)
        server_thread.daemon = True
        server_thread.start()
        return sock

    def setup_smtp_server(self, port: int, handler_data: Dict):
        class CustomSMTPServer(smtplib.SMTP):
            def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
                return json.dumps(handler_data)

        server = CustomSMTPServer(("0.0.0.0", port))
        threading.Thread(target=server.serve_forever).start()
        return server

    def setup_sftp_server(self, port: int, handler_data: Dict):
        class SFTPServer(paramiko.ServerInterface):
            def check_auth_password(self, username, password):
                return paramiko.AUTH_SUCCESSFUL

        server = paramiko.Transport(("0.0.0.0", port))
        server.add_server_key(paramiko.RSAKey.generate(2048))
        server.start_server(server=SFTPServer())
        return server

    async def create_endpoint(self, uri: str, protocol: ProtocolType, port: int, handler_data: Dict[str, Any]):
        self.endpoints[uri] = EndpointConfig(uri, protocol, port, handler_data)

        if protocol == ProtocolType.HTTP:
            async def dynamic_endpoint():
                return handler_data

            self.http_app.get(f"/{uri}")(dynamic_endpoint)

        elif protocol == ProtocolType.FTP:
            self.servers[uri] = await self.start_ftp_server(port, handler_data.get("directory", "./"))

        elif protocol == ProtocolType.RTSP:
            self.servers[uri] = await self.start_rtsp_server(port)

        elif protocol == ProtocolType.MQTT:
            self.servers[uri] = await self.start_mqtt_broker(port)

        elif protocol == ProtocolType.WEBSOCKET:
            self.servers[uri] = await self.start_websocket_server(port, handler_data)

        elif protocol == ProtocolType.TCP:
            self.servers[uri] = self.start_tcp_server(port, handler_data)

        elif protocol == ProtocolType.UDP:
            self.servers[uri] = self.start_udp_server(port, handler_data)

        elif protocol == ProtocolType.SMTP:
            self.servers[uri] = self.setup_smtp_server(port, handler_data)

        elif protocol == ProtocolType.SFTP:
            self.servers[uri] = self.setup_sftp_server(port, handler_data)

    def save_config(self):
        config = {
            uri: {
                'protocol': endpoint.protocol,
                'port': endpoint.port,
                'handler_data': endpoint.handler_data
            }
            for uri, endpoint in self.endpoints.items()
        }
        with open(self.config_file, 'w') as file:
            yaml.dump(config, file)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file) or {}
                for uri, data in config.items():
                    self.endpoints[uri] = EndpointConfig(
                        uri=uri,
                        protocol=ProtocolType(data['protocol']),
                        port=data['port'],
                        handler_data=data['handler_data']
                    )


async def main():
    parser = argparse.ArgumentParser(description="URIPoint - Multi-Protocol Endpoint Creator")
    parser.add_argument('--uri', type=str, help="Endpoint URI")
    parser.add_argument('--protocol', type=str,
                        choices=['http', 'ftp', 'rtsp', 'mqtt', 'ws', 'tcp', 'udp', 'smtp', 'sftp'],
                        help="Protocol type")
    parser.add_argument('--port', type=int, help="Port number")
    parser.add_argument('--data', type=str, help="Handler data in JSON format")
    parser.add_argument('--list', action='store_true', help="List all endpoints")
    parser.add_argument('--serve', action='store_true', help="Start all servers")

    args = parser.parse_args()
    server = MultiProtocolServer()
    server.load_config()

    if args.list:
        print("\nConfigured Endpoints:")
        print("-------------------")
        for uri, endpoint in server.endpoints.items():
            print(f"\nURI: {uri}")
            print(f"Protocol: {endpoint.protocol}")
            print(f"Port: {endpoint.port}")
            print(f"Handler Data: {json.dumps(endpoint.handler_data, indent=2)}")
        return

    if args.serve:
        print("Starting all protocol servers...")
        for uri, endpoint in server.endpoints.items():
            await server.create_endpoint(
                uri=endpoint.uri,
                protocol=endpoint.protocol,
                port=endpoint.port,
                handler_data=endpoint.handler_data
            )
        print("All servers started successfully!")
        # Keep the main thread running
        await asyncio.Event().wait()
        return

    if args.uri and args.protocol and args.port:
        try:
            handler_data = json.loads(args.data) if args.data else {"message": "Default response"}
            await server.create_endpoint(args.uri, ProtocolType(args.protocol), args.port, handler_data)
            server.save_config()
            print(f"\nEndpoint created successfully!")
            print(f"Protocol: {args.protocol}")
            print(f"URI: {args.uri}")
            print(f"Port: {args.port}")
            print(f"Handler data: {json.dumps(handler_data, indent=2)}")
        except Exception as e:
            print(f"Error creating endpoint: {e}")
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())