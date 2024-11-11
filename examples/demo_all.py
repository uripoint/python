"""
Comprehensive demo script showing all UriPoint capabilities
"""
import subprocess
import time
from uripoint import UriPointCLI

def run_command(command):
    """Run shell command and print output"""
    print(f"\n$ {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result

def setup_and_test_endpoints():
    """Setup and test all example endpoints"""
    print("\n=== Setting up and testing all endpoints ===\n")

    # 1. REST API
    print("\n=== REST API Example ===")
    run_command('uripoint --uri http://localhost:8000/api/users --data \'{"response": {"users": [{"id": 1, "name": "John"}]}}\' --method GET POST')
    time.sleep(1)  # Wait for endpoint to be ready
    run_command('curl -X GET http://localhost:8000/api/users')
    run_command('curl -X POST http://localhost:8000/api/users -H "Content-Type: application/json" -d \'{"name": "Alice"}\'')

    # 2. Authentication
    print("\n=== Authentication Example ===")
    run_command('uripoint --uri http://localhost:8000/auth/login --data \'{"response": {"token": "eyJ0eXAi..."}}\' --method POST')
    run_command('curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"username": "admin", "password": "secret"}\'')

    # 3. CRUD Operations
    print("\n=== CRUD Operations Example ===")
    run_command('uripoint --uri http://localhost:8000/api/products --data \'{"response": {"products": []}, "methods": ["GET", "POST", "PUT", "DELETE"]}\' --method GET POST PUT DELETE')
    run_command('curl -X GET http://localhost:8000/api/products')
    run_command('curl -X POST http://localhost:8000/api/products -H "Content-Type: application/json" -d \'{"name": "Product 1"}\'')
    run_command('curl -X PUT http://localhost:8000/api/products/1 -H "Content-Type: application/json" -d \'{"name": "Updated Product"}\'')
    run_command('curl -X DELETE http://localhost:8000/api/products/1')

    # 4. Streaming Media
    print("\n=== Streaming Media Example ===")
    run_command('uripoint --uri rtsp://localhost:8554/camera1 --data \'{"stream_url": "rtsp://camera.example.com/stream1", "transport": "tcp"}\'')
    print("To test: ffplay rtsp://localhost:8554/camera1")

    # 5. IoT Sensors
    print("\n=== IoT Sensors Example ===")
    run_command('uripoint --uri mqtt://localhost:1883/sensors/temperature --data \'{"topic": "sensors/temperature", "qos": 1, "device": {"type": "temperature", "location": "room1"}}\'')
    print("To test: mosquitto_pub -h localhost -p 1883 -t sensors/temperature -m '{\"value\": 22.5}'")

    # 6. Message Queue
    print("\n=== Message Queue Example ===")
    run_command('uripoint --uri amqp://localhost:5672/orders --data \'{"exchange": "orders", "queue": "new_orders", "routing_key": "order.new"}\'')
    run_command('curl -X POST http://localhost:5672/orders -H "Content-Type: application/json" -d \'{"order_id": "123", "items": ["item1", "item2"]}\'')

    # 7. Cache System
    print("\n=== Cache System Example ===")
    run_command('uripoint --uri redis://localhost:6379/cache --data \'{"db": 0, "decode_responses": true}\'')
    run_command('curl -X GET http://localhost:6379/cache/user:123')
    run_command('curl -X PUT http://localhost:6379/cache/user:123 -d \'{"name": "John", "age": 30}\'')

    # 8. Email Service
    print("\n=== Email Service Example ===")
    run_command('uripoint --uri smtp://localhost:587/mail --data \'{"use_tls": true, "timeout": 30}\'')
    run_command('curl -X POST http://localhost:587/mail -H "Content-Type: application/json" -d \'{"to": "user@example.com", "subject": "Test", "body": "Hello World"}\'')

    # 9. DNS Service
    print("\n=== DNS Service Example ===")
    run_command('uripoint --uri dns://localhost:53/lookup --data \'{"timeout": 5, "cache_enabled": true}\'')
    run_command('curl -X GET "http://localhost:53/lookup?domain=example.com"')

    # 10. WebSocket Chat
    print("\n=== WebSocket Chat Example ===")
    run_command('uripoint --uri ws://localhost:8080/chat --data \'{"protocol": "chat", "max_connections": 100}\'')
    print("To test: wscat -c ws://localhost:8080/chat")

    # 11. Monitoring System
    print("\n=== Monitoring System Example ===")
    run_command('uripoint --uri http://localhost:9090/metrics --data \'{"response": {"cpu_usage": 45, "memory_usage": 60, "disk_space": 80}}\' --method GET')
    run_command('curl -X GET http://localhost:9090/metrics')

    # 12. File Storage
    print("\n=== File Storage Example ===")
    run_command('uripoint --uri http://localhost:8000/storage --data \'{"base_path": "/tmp/storage", "max_size": "100M"}\' --method GET POST DELETE')
    run_command('echo "test" > test.txt')
    run_command('curl -X POST http://localhost:8000/storage -F "file=@test.txt"')
    run_command('curl -X GET http://localhost:8000/storage/test.txt')
    run_command('curl -X DELETE http://localhost:8000/storage/test.txt')
    run_command('rm test.txt')

    # 13. GraphQL API
    print("\n=== GraphQL API Example ===")
    run_command('uripoint --uri http://localhost:4000/graphql --data \'{"schema": "type Query { users: [User] }", "resolvers": {"Query": {"users": []}}}\' --method POST')
    run_command('curl -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d \'{"query": "{ users { id name } }"}\'')

    # 14. Load Balancer
    print("\n=== Load Balancer Example ===")
    run_command('uripoint --uri http://localhost:8001/api --data \'{"response": {"server": "1"}}\'')
    run_command('uripoint --uri http://localhost:8002/api --data \'{"response": {"server": "2"}}\'')
    run_command('curl -X GET http://localhost:8001/api')
    run_command('curl -X GET http://localhost:8002/api')

    # 15. Event Stream
    print("\n=== Event Stream Example ===")
    run_command('uripoint --uri http://localhost:8000/events --data \'{"response": {"type": "sse"}, "headers": {"Content-Type": "text/event-stream"}}\'')
    print("To test: curl -N http://localhost:8000/events")

    print("\n=== All examples completed ===")

if __name__ == '__main__':
    setup_and_test_endpoints()
