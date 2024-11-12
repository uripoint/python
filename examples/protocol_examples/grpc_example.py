"""
Example demonstrating gRPC protocol support in UriPoint
"""
from uripoint import UriPointCLI

def setup_grpc_endpoints():
    """Setup gRPC service endpoints"""
    cli = UriPointCLI()

    # User service
    cli.create_endpoint(
        uri='grpc://localhost:50051/users',
        data={
            'proto_file': 'users.proto',
            'service': 'UserService',
            'methods': {
                'GetUser': {
                    'input': 'UserRequest',
                    'output': 'UserResponse'
                },
                'CreateUser': {
                    'input': 'CreateUserRequest',
                    'output': 'UserResponse'
                },
                'UpdateUser': {
                    'input': 'UpdateUserRequest',
                    'output': 'UserResponse'
                }
            },
            'streaming': {
                'UserUpdates': {
                    'type': 'server_streaming',
                    'input': 'UserStreamRequest',
                    'output': 'UserStreamResponse'
                }
            }
        }
    )

    # Product service
    cli.create_endpoint(
        uri='grpc://localhost:50052/products',
        data={
            'proto_file': 'products.proto',
            'service': 'ProductService',
            'methods': {
                'GetProduct': {
                    'input': 'ProductRequest',
                    'output': 'ProductResponse'
                },
                'SearchProducts': {
                    'input': 'SearchRequest',
                    'output': 'SearchResponse',
                    'streaming': 'server'
                }
            }
        }
    )

    # Order service with bidirectional streaming
    cli.create_endpoint(
        uri='grpc://localhost:50053/orders',
        data={
            'proto_file': 'orders.proto',
            'service': 'OrderService',
            'methods': {
                'PlaceOrder': {
                    'input': 'OrderRequest',
                    'output': 'OrderResponse'
                }
            },
            'streaming': {
                'OrderStream': {
                    'type': 'bidirectional',
                    'input': 'OrderStreamRequest',
                    'output': 'OrderStreamResponse'
                }
            }
        }
    )

    print("\ngRPC endpoints created:")
    print("1. User Service:")
    print("   - URI: grpc://localhost:50051/users")
    print("   - Methods: GetUser, CreateUser, UpdateUser")
    print("   - Streaming: UserUpdates")
    
    print("\n2. Product Service:")
    print("   - URI: grpc://localhost:50052/products")
    print("   - Methods: GetProduct, SearchProducts")
    
    print("\n3. Order Service:")
    print("   - URI: grpc://localhost:50053/orders")
    print("   - Methods: PlaceOrder")
    print("   - Streaming: OrderStream (bidirectional)")

def test_grpc_endpoints():
    """Test gRPC endpoints"""
    cli = UriPointCLI()

    # Test user service
    user_request = {
        'id': '123',
        'fields': ['name', 'email']
    }
    cli.publish('grpc://localhost:50051/users/GetUser', user_request)

    # Test product service
    search_request = {
        'query': 'electronics',
        'page_size': 10
    }
    cli.publish('grpc://localhost:50052/products/SearchProducts', search_request)

    # Test order service
    order_request = {
        'user_id': '123',
        'items': [
            {'product_id': 'p1', 'quantity': 2},
            {'product_id': 'p2', 'quantity': 1}
        ]
    }
    cli.publish('grpc://localhost:50053/orders/PlaceOrder', order_request)

if __name__ == '__main__':
    print("Setting up gRPC endpoints...")
    setup_grpc_endpoints()
    
    print("\nTesting gRPC endpoints...")
    test_grpc_endpoints()
