"""
Redis Protocol Example for UriPoint
Demonstrates using Redis for caching and data storage
"""

from uripoint import UriPointCLI

def setup_redis_endpoints():
    # Create CLI instance
    cli = UriPointCLI()

    # Create Redis endpoint for user cache
    cli.create_endpoint(
        uri='redis://localhost:6379/users',
        data={
            'db': 0,
            'decode_responses': True,
            'max_connections': 10
        }
    )

    # Create Redis endpoint for session storage
    cli.create_endpoint(
        uri='redis://localhost:6379/sessions',
        data={
            'db': 1,
            'decode_responses': True,
            'expire': 3600  # 1 hour expiry
        }
    )

def demonstrate_redis_operations():
    cli = UriPointCLI()
    
    # Store user data
    user_data = {
        'id': '12345',
        'name': 'John Doe',
        'email': 'john@example.com'
    }
    cli.set('redis://localhost:6379/users/12345', user_data)
    
    # Store session data
    session_data = {
        'user_id': '12345',
        'login_time': '2023-07-20T10:00:00',
        'last_active': '2023-07-20T10:30:00'
    }
    cli.set('redis://localhost:6379/sessions/sess_abc123', session_data)
    
    # Retrieve data
    user = cli.get('redis://localhost:6379/users/12345')
    session = cli.get('redis://localhost:6379/sessions/sess_abc123')
    
    print(f"Retrieved user: {user}")
    print(f"Retrieved session: {session}")

if __name__ == '__main__':
    setup_redis_endpoints()
    demonstrate_redis_operations()
