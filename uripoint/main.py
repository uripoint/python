import argparse
import yaml
import json
import sys

class UriPointCLI:
    def __init__(self):
        self.endpoints = []
        self.config_file = 'uripoint_config.yaml'

    def create_endpoint(self, uri, protocol, port, data):
        """Create a new endpoint configuration"""
        endpoint = {
            'uri': uri,
            'protocol': protocol,
            'port': port,
            'data': json.loads(data) if data else {}
        }
        self.endpoints.append(endpoint)
        self._save_config()
        print(f"Endpoint created: {uri} ({protocol}:{port})")

    def list_endpoints(self):
        """List all configured endpoints"""
        if not self.endpoints:
            print("No endpoints configured.")
            return
        
        for idx, endpoint in enumerate(self.endpoints, 1):
            print(f"{idx}. {endpoint['uri']} - {endpoint['protocol']}:{endpoint['port']}")

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
            print("No endpoints to serve. Use --uri to create endpoints first.")
            return

        print("Starting endpoints:")
        for endpoint in self.endpoints:
            print(f"- {endpoint['uri']} ({endpoint['protocol']}:{endpoint['port']})")

def main():
    parser = argparse.ArgumentParser(description="UriPoint: Endpoint Management CLI")
    parser.add_argument('--uri', help='Endpoint URI')
    parser.add_argument('--protocol', choices=[
        'http', 'ftp', 'rtsp', 'mqtt', 'ws', 'tcp', 'udp', 'smtp', 'pop3', 'sftp'
    ], help='Protocol for the endpoint')
    parser.add_argument('--port', type=int, help='Port number')
    parser.add_argument('--data', help='JSON-formatted data for the endpoint')
    parser.add_argument('--serve', action='store_true', help='Serve all configured endpoints')
    parser.add_argument('--list', action='store_true', help='List all configured endpoints')

    args = parser.parse_args()
    cli = UriPointCLI()

    if args.serve:
        cli.serve()
    elif args.list:
        cli.list_endpoints()
    elif args.uri and args.protocol and args.port:
        cli.create_endpoint(args.uri, args.protocol, args.port, args.data)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
