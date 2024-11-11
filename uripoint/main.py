"""
Main entry point for UriPoint CLI
"""
import argparse
import json
import yaml
import os
from typing import Dict, Any, List
from .cli import UriPointCLI

def load_config() -> Dict[str, Any]:
    """
    Load configuration from YAML file
    """
    config_path = os.path.expanduser('~/.uripoint_config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return config if isinstance(config, dict) else {'endpoints': {}}
    return {'endpoints': {}}

def save_config(config: Dict[str, Any]) -> None:
    """
    Save configuration to YAML file
    """
    config_path = os.path.expanduser('~/.uripoint_config.yaml')
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

def detach_endpoints(config: Dict[str, Any], endpoints: List[str] = None) -> Dict[str, Any]:
    """
    Detach specified endpoints or all if none specified
    
    :param config: Current configuration
    :param endpoints: List of endpoint URIs to detach, or None for all
    :return: Updated configuration
    """
    if not endpoints:
        print("Detaching all endpoints...")
        config['endpoints'] = {}
    else:
        print(f"Detaching specified endpoints: {endpoints}")
        for uri in endpoints:
            if uri in config.get('endpoints', {}):
                del config['endpoints'][uri]
                print(f"Detached: {uri}")
            else:
                print(f"Endpoint not found: {uri}")
    return config

def main():
    parser = argparse.ArgumentParser(description='UriPoint CLI')
    
    # Add arguments
    parser.add_argument('--uri', help='Full URI for endpoint')
    parser.add_argument('--hostname', help='Hostname for endpoint')
    parser.add_argument('--path', help='Path for endpoint')
    parser.add_argument('--protocol', help='Protocol for endpoint')
    parser.add_argument('--port', type=int, help='Port for endpoint')
    parser.add_argument('--data', help='Configuration data for endpoint')
    parser.add_argument('--method', nargs='+', help='HTTP methods to allow (GET, POST, etc.)')
    parser.add_argument('--list', action='store_true', help='List all endpoints')
    parser.add_argument('--serve', action='store_true', help='Serve all endpoints')
    parser.add_argument('--test', action='store_true', help='Test endpoints')
    parser.add_argument('--detach', nargs='*', help='Detach endpoints (specify URIs or omit for all)')
    
    args = parser.parse_args()
    cli = UriPointCLI()
    
    # Load existing configuration
    config = load_config()

    if args.detach is not None:
        config = detach_endpoints(config, args.detach if args.detach else None)
        save_config(config)
        print("Detach operation completed.")
        return
    
    # Restore endpoints from config
    for uri, data in config.get('endpoints', {}).items():
        cli.create_endpoint(uri, data)
    
    if args.list:
        # List all endpoints
        endpoints = cli.list_endpoints()
        print("\nConfigured Endpoints:")
        for endpoint in endpoints:
            print(f"\nProtocol: {endpoint['protocol']}")
            print(f"Hostname: {endpoint['hostname']}")
            print(f"Port: {endpoint['port']}")
            print(f"Path: {endpoint['path']}")
            
            # Show allowed methods for HTTP/HTTPS endpoints
            if endpoint['protocol'] in ['http', 'https']:
                uri = f"{endpoint['protocol']}://{endpoint['hostname']}:{endpoint['port']}{endpoint['path']}"
                endpoint_config = cli.get_endpoint(uri)
                if endpoint_config:
                    methods = endpoint_config.get('config', {}).get('methods', ['GET'])
                    print(f"Methods: {', '.join(methods)}")
        return

    if args.serve:
        # Serve all endpoints
        print("\nStarting servers...")
        try:
            cli.serve()
        except KeyboardInterrupt:
            print("\nShutting down servers...")
        return

    if args.test:
        # Test endpoints
        endpoints = cli.list_endpoints()
        print("\nTesting Endpoints:")
        for endpoint in endpoints:
            uri = f"{endpoint['protocol']}://{endpoint['hostname']}:{endpoint['port']}{endpoint['path']}"
            try:
                result = cli.get_endpoint(uri)
                status = "OK" if result else "Failed"
                print(f"{uri}: {status}")
                if result and endpoint['protocol'] in ['http', 'https']:
                    methods = result.get('config', {}).get('methods', ['GET'])
                    print(f"  Allowed methods: {', '.join(methods)}")
            except Exception as e:
                print(f"{uri}: Error - {str(e)}")
        return

    # Create new endpoint
    if args.uri or (args.hostname and args.protocol):
        # Parse endpoint data
        data = {}
        if args.data:
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON data")
                return

        # Add HTTP methods if specified
        if args.method:
            if not isinstance(data, dict):
                data = {}
            data['methods'] = [m.upper() for m in args.method]

        # Create endpoint from full URI
        if args.uri:
            uri = args.uri
        else:
            # Create endpoint from components
            port = args.port or {'http': 80, 'https': 443}.get(args.protocol, 8000)
            path = args.path or '/'
            uri = f"{args.protocol}://{args.hostname}:{port}{path}"

        try:
            cli.create_endpoint(uri, data)
            print(f"Created endpoint: {uri}")
            if args.method:
                print(f"Allowed methods: {', '.join(data['methods'])}")
            
            # Update configuration
            if 'endpoints' not in config:
                config['endpoints'] = {}
            config['endpoints'][uri] = data
            save_config(config)
            
        except ValueError as e:
            print(f"Error: {str(e)}")
            return

if __name__ == '__main__':
    main()
