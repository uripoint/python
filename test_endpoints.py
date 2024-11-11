"""
Test script to verify endpoints with different HTTP methods
"""
import requests
import json

def test_endpoints():
    # Test cases with different HTTP methods
    test_cases = [
        # GET requests
        ('GET', 'http://localhost:9000/api/hello'),
        ('GET', 'http://localhost:9000/api/status'),
        ('GET', 'http://localhost:9000/api/users'),
        ('GET', 'http://localhost:9001/metrics'),
        
        # POST requests
        ('POST', 'http://localhost:9000/api/hello'),
        ('POST', 'http://localhost:9000/api/users'),
        
        # PUT request (should work for /api/users)
        ('PUT', 'http://localhost:9000/api/users'),
        
        # DELETE request (should work for /api/users)
        ('DELETE', 'http://localhost:9000/api/users'),
        
        # Methods that should fail
        ('POST', 'http://localhost:9000/api/status'),  # Should fail (GET only)
        ('PUT', 'http://localhost:9000/api/hello'),    # Should fail (GET, POST only)
    ]

    for method, endpoint in test_cases:
        try:
            print(f"\nTesting {method} {endpoint}...")
            response = requests.request(method, endpoint)
            print(f"Status code: {response.status_code}")
            print("Response:")
            try:
                print(json.dumps(response.json(), indent=2))
            except json.JSONDecodeError:
                print(response.text)
            print(f"Allowed methods: {response.headers.get('Access-Control-Allow-Methods', 'Not specified')}")
        except Exception as e:
            print(f"Error: {str(e)}")

    # Test OPTIONS request
    print("\nTesting OPTIONS request...")
    for endpoint in ['http://localhost:9000/api/users', 'http://localhost:9000/api/hello']:
        try:
            response = requests.options(endpoint)
            print(f"\nOPTIONS {endpoint}")
            print(f"Status code: {response.status_code}")
            print(f"Allowed methods: {response.headers.get('Access-Control-Allow-Methods', 'Not specified')}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == '__main__':
    print("Testing UriPoint endpoints with different HTTP methods...")
    test_endpoints()
    print("\nTest complete.")
