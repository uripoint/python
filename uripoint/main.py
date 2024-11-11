import argparse
import json
import sys
import yaml
from urllib.parse import urlparse

class UriPointCLI:
    def __init__(self):
        self.endpoints = []
        self.config_file = 'uripoint_config.yaml'

    def parse_uri(self, uri=None, hostname=None, path=None, protocol=None, port=None):
        """
        Parse URI or construct from components
        
        :param uri: Full URI
        :param hostname: Hostname
        :param path: Path
        :param protocol: Protocol
        :param port: Port
        :return: Parsed URI details
        """
        if uri:
            parsed = urlparse(uri)
            return {
                'protocol': parsed.scheme or 'http',
                'hostname': parsed.hostname or 'localhost',
                'path': parsed.path,
                'port': parsed.port or 80
            }
        
        return {
            'protocol': protocol or 'http',
            'hostname': hostname or 'localhost',
            'path': path or '/',
            'port': port or 8000
        }

    def create_endpoint(self, uri=None, hostname=None, path=None, protocol=None, port=None, data=None):
        """
        Create a new endpoint configuration
        
        :param uri: Full URI
        :param hostname: Hostname
        :param path: Path
        :param protocol: Protocol
        :param port: Port
        :param data: Endpoint data
        """
        endpoint_details = self.parse_uri(uri, hostname, path, protocol, port)
        
        endpoint = {
            **endpoint_details,
            'data': json.loads(data) if data else {}
        }
        
        self.endpoints.append(endpoint)
        self._save_config()
        
        print(f"Endpoint created: {endpoint['protocol']}://{endpoint['hostname']}:{endpoint['port']}{endpoint['path']}")
        print(f"Data: {endpoint['data']}")

    def list_endpoints(self):
        """List all configured endpoints"""
        if not self.endpoints:
            print("No endpoints configured.")
            return
        
        for idx, endpoint in enumerate(self.endpoints, 1):
            print(f"{idx}. {endpoint['protocol']}://{endpoint['hostname']}:{endpoint['port']}{endpoint['path']}")
            print(f"   Data: {endpoint['data']}\n")

    def _save_config(self):
        """Save endpoints to YAML configuration file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.endpoints, f)

    def _load_config(self):
        """Load endpoints from YAML configuration file"""
        try:
            with open(self.config_file, 'r') as f:
                self.endpoints = yaml.safe_load(f) or []
        except FileNotFoundError:
            self.endpoints = []

    def serve(self):
        """Simulate serving all configured endpoints"""
        self._load_config()
        if not self.endpoints:
            print("No endpoints to serve. Use --uri or other options to create endpoints first.")
            return

        print("Starting endpoints:")
        for endpoint in self.endpoints:
            print(f"- {endpoint['protocol']}://{endpoint['hostname']}:{endpoint['port']}{endpoint['path']}")

def main():
    parser = argparse.ArgumentParser(description="UriPoint: Flexible Endpoint Management CLI")
    
    # URI or component-based endpoint creation
    parser.add_argument('--uri', help='Full URI (e.g., http://localhost:8080/api/status)')
    parser.add_argument('--hostname', help='Hostname (default: localhost)')
    parser.add_argument('--path', help='Endpoint path (default: /)')
    parser.add_argument('--protocol', help='Protocol (default: http)', 
                        choices=['http', 'https', 'ws', 'wss', 'ftp', 'sftp'])
    parser.add_argument('--port', type=int, help='Port number (default: 8000)')
    
    # Data and action arguments
    parser.add_argument('--data', help='JSON-formatted data for the endpoint')
    parser.add_argument('--serve', action='store_true', help='Serve all configured endpoints')
    parser.add_argument('--list', action='store_true', help='List all configured endpoints')

    args = parser.parse_args()
    cli = UriPointCLI()

    if args.serve:
        cli.serve()
    elif args.list:
        cli.list_endpoints()
    elif args.uri or (args.hostname and args.path):
        cli.create_endpoint(
            uri=args.uri, 
            hostname=args.hostname, 
            path=args.path, 
            protocol=args.protocol, 
            port=args.port, 
            data=args.data
        )
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
