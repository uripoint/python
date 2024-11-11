#!/usr/bin/env python3
"""
Example usage of UriPoint StreamFilterRouter
"""

from uripoint.router import StreamFilterRouter, get_url_parts, extract_query_params

def main():
    # Create a new router
    router = StreamFilterRouter()

    # Define a simple route handler for API status
    def api_status_handler(data):
        print(f"API Status Handler received: {data}")
        return {"status": "OK", "data": data}

    # Define a simple route handler for user information
    def user_info_handler(data):
        print(f"User Info Handler received: {data}")
        return {"user": "example_user", "data": data}

    # Add routes with regex patterns
    router.add_route(r'^/api/status$', api_status_handler)
    router.add_route(r'^/api/user/.*', user_info_handler)

    # Define a simple filter to uppercase data
    def uppercase_filter(data):
        if isinstance(data, str):
            return data.upper()
        return data

    # Add a filter
    router.add_filter('uppercase', uppercase_filter)

    # Test route matching and processing
    print("\nTesting /api/status route:")
    result = router.process('/api/status', 'test data')
    print("Result:", result)

    print("\nTesting /api/user/profile route:")
    result = router.process('/api/user/profile', 'user data')
    print("Result:", result)

    # Demonstrate URL parsing utilities
    test_url = 'https://example.com/path?name=john&age=30'
    print("\nURL Parts:")
    print(get_url_parts(test_url))

    print("\nQuery Parameters:")
    print(extract_query_params(test_url))

if __name__ == '__main__':
    main()
