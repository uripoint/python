"""
CLI interface for UriPoint
"""
from typing import Dict, Any, List, Optional
import http.server
import socketserver
import threading
import json
from .router import StreamFilterRouter, get_url_parts
from .protocols import get_protocol_handler

class EndpointHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, router=None, **kwargs):
        self.router = router
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        """Override to provide more detailed logging"""
        print(f"[{self.log_date_time_string()}] {format%args}")

    def handle_endpoint(self):
        """Handle endpoint request for any HTTP method"""
        if self.router:
            # Get endpoint that matches the path
            endpoints = self.router.get_endpoints()
            print(f"Available endpoints: {[info['path'] for info in endpoints.values()]}")
            
            for uri, info in endpoints.items():
                if info['path'] == self.path:
                    print(f"Found matching endpoint: {uri}")
                    # Handle based on protocol
                    handler = get_protocol_handler(info['protocol'])
                    if handler:
                        try:
                            response = handler.handle_request(info, method=self.command)
                            print(f"Handler response: {response}")
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            
                            # Add CORS headers
                            self.send_header('Access-Control-Allow-Origin', '*')
                            self.send_header('Access-Control-Allow-Methods', 
                                          ', '.join(info.get('config', {}).get('methods', ['GET'])))
                            
                            self.end_headers()
                            self.wfile.write(response.encode())
                            return True
                        except ValueError as e:
                            print(f"Method not allowed: {str(e)}")
                            self.send_error(405, str(e))
                            return True
                        except Exception as e:
                            print(f"Error handling request: {str(e)}")
                            self.send_error(500, str(e))
                            return True

        print(f"No endpoint found for path: {self.path}")
        self.send_error(404, "Endpoint not found")
        return True

    def do_GET(self):
        """Handle GET requests"""
        print(f"\nReceived GET request for: {self.path}")
        self.handle_endpoint()

    def do_POST(self):
        """Handle POST requests"""
        print(f"\nReceived POST request for: {self.path}")
        self.handle_endpoint()

    def do_PUT(self):
        """Handle PUT requests"""
        print(f"\nReceived PUT request for: {self.path}")
        self.handle_endpoint()

    def do_DELETE(self):
        """Handle DELETE requests"""
        print(f"\nReceived DELETE request for: {self.path}")
        self.handle_endpoint()

    def do_PATCH(self):
        """Handle PATCH requests"""
        print(f"\nReceived PATCH request for: {self.path}")
        self.handle_endpoint()

    def do_OPTIONS(self):
        """Handle OPTIONS requests"""
        print(f"\nReceived OPTIONS request for: {self.path}")
        if self.router:
            endpoints = self.router.get_endpoints()
            for uri, info in endpoints.items():
                if info['path'] == self.path:
                    methods = info.get('config', {}).get('methods', ['GET'])
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', ', '.join(methods))
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                    self.end_headers()
                    return
        self.send_error(404, "Endpoint not found")

class UriPointCLI:
    def __init__(self):
        self.router = StreamFilterRouter()
        self.servers = {}
    
    def create_endpoint(self, uri: str, data: Dict[str, Any]) -> bool:
        """
        Create a new endpoint
        
        :param uri: URI for the endpoint
        :param data: Configuration data for the endpoint
        :return: Success status
        """
        try:
            return self.router.add_endpoint(uri, data)
        except ValueError as e:
            raise ValueError(f"Failed to create endpoint: {str(e)}")
    
    def list_endpoints(self) -> List[Dict[str, Any]]:
        """
        List all registered endpoints
        
        :return: List of endpoint configurations
        """
        endpoints = self.router.get_endpoints()
        return [
            {
                'protocol': info['protocol'],
                'hostname': info['hostname'],
                'port': info['port'],
                'path': info['path']
            }
            for info in endpoints.values()
        ]
    
    def get_endpoint(self, uri: str) -> Optional[Dict[str, Any]]:
        """
        Get endpoint configuration by URI
        
        :param uri: URI of the endpoint
        :return: Endpoint configuration if found
        """
        endpoints = self.router.get_endpoints()
        return endpoints.get(uri)
    
    def publish(self, uri: str, data: Any) -> bool:
        """
        Publish data to an endpoint
        
        :param uri: URI of the endpoint
        :param data: Data to publish
        :return: Success status
        """
        return bool(self.router.process(uri, data))
    
    def subscribe(self, uri: str, callback: callable) -> bool:
        """
        Subscribe to an endpoint
        
        :param uri: URI of the endpoint
        :param callback: Callback function for received data
        :return: Success status
        """
        pattern = get_url_parts(uri)['path']
        self.router.add_route(pattern, callback)
        return True
    
    def serve(self) -> None:
        """
        Start serving all endpoints
        """
        endpoints = self.router.get_endpoints()
        print(f"\nRegistered endpoints: {[info['path'] for info in endpoints.values()]}")
        
        # Group endpoints by port
        port_groups = {}
        for uri, info in endpoints.items():
            port = info.get('port', 80)
            if port not in port_groups:
                port_groups[port] = []
            port_groups[port].append(info)
        
        # Create servers for each port
        for port, endpoints in port_groups.items():
            def create_handler(*args, **kwargs):
                return EndpointHandler(*args, router=self.router, **kwargs)
            
            try:
                server = socketserver.TCPServer(('', port), create_handler)
                print(f"\nStarting server on port {port}")
                print(f"Endpoints on port {port}:")
                for endpoint in endpoints:
                    methods = endpoint.get('config', {}).get('methods', ['GET'])
                    print(f"  {endpoint['path']} [{', '.join(methods)}]")
                
                # Start server in a new thread
                thread = threading.Thread(target=server.serve_forever)
                thread.daemon = True
                thread.start()
                
                self.servers[port] = server
            except Exception as e:
                print(f"Failed to start server on port {port}: {str(e)}")
        
        print("\nAll servers started. Press Ctrl+C to stop.")
        
        # Keep main thread running
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_servers()
    
    def stop_servers(self) -> None:
        """
        Stop all running servers
        """
        for port, server in self.servers.items():
            print(f"Stopping server on port {port}")
            server.shutdown()
            server.server_close()
        self.servers.clear()
