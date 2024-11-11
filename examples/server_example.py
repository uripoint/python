"""
Example demonstrating UriPoint server functionality
"""
import os
import sys

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uripoint import UriPointCLI

def setup_test_endpoints():
    cli = UriPointCLI()

    # Create a simple HTTP endpoint
    cli.create_endpoint(
        uri='http://localhost:8000/api/hello',
        data={
            'response': {'message': 'Hello from UriPoint!'},
            'content_type': 'application/json'
        }
    )

    # Create another endpoint on the same port
    cli.create_endpoint(
        uri='http://localhost:8000/api/status',
        data={
            'response': {'status': 'OK', 'version': '1.1.0'},
            'content_type': 'application/json'
        }
    )

    # Create an endpoint on a different port
    cli.create_endpoint(
        uri='http://localhost:8001/metrics',
        data={
            'response': {
                'uptime': '1h 30m',
                'requests': 150,
                'errors': 0
            },
            'content_type': 'application/json'
        }
    )

    print("Test endpoints created. Run 'uripoint --serve' to start the server.")
    print("\nAvailable endpoints:")
    print("- http://localhost:8000/api/hello")
    print("- http://localhost:8000/api/status")
    print("- http://localhost:8001/metrics")

if __name__ == '__main__':
    setup_test_endpoints()
