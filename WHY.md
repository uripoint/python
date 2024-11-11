# Why UriPoint?

[Previous content remains unchanged until "Examples" section...]

## Praktyczne Przykłady

### 1. REST API Endpoints

```bash
# Utworzenie endpointu użytkowników
uripoint --uri http://localhost:8000/api/users --data '{"response": {"users": [{"id": 1, "name": "John"}]}}' --method GET POST

# Test endpointu
curl -X GET http://localhost:8000/api/users
curl -X POST http://localhost:8000/api/users -H "Content-Type: application/json" -d '{"name": "Alice"}'
```

### 2. Autentykacja

```bash
# Endpoint logowania
uripoint --uri http://localhost:8000/auth/login --data '{"response": {"token": "eyJ0eXAi..."}}' --method POST

# Test logowania
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'
```

### 3. CRUD Operations

```bash
# Endpoint produktów z pełnym CRUD
uripoint --uri http://localhost:8000/api/products --data '{
  "response": {"products": []},
  "methods": ["GET", "POST", "PUT", "DELETE"]
}' --method GET POST PUT DELETE

# Testy CRUD
curl -X GET http://localhost:8000/api/products
curl -X POST http://localhost:8000/api/products -H "Content-Type: application/json" -d '{"name": "Product 1"}'
curl -X PUT http://localhost:8000/api/products/1 -H "Content-Type: application/json" -d '{"name": "Updated Product"}'
curl -X DELETE http://localhost:8000/api/products/1
```

### 4. Streaming Media

```bash
# Endpoint RTSP kamery
uripoint --uri rtsp://localhost:8554/camera1 --data '{
  "stream_url": "rtsp://camera.example.com/stream1",
  "transport": "tcp"
}'

# Test streamu
ffplay rtsp://localhost:8554/camera1
```

### 5. IoT Sensors

```bash
# Endpoint czujnika temperatury
uripoint --uri mqtt://localhost:1883/sensors/temperature --data '{
  "topic": "sensors/temperature",
  "qos": 1,
  "device": {"type": "temperature", "location": "room1"}
}'

# Test publikacji danych
mosquitto_pub -h localhost -p 1883 -t sensors/temperature -m '{"value": 22.5}'
```

### 6. Message Queue

```bash
# Endpoint kolejki wiadomości
uripoint --uri amqp://localhost:5672/orders --data '{
  "exchange": "orders",
  "queue": "new_orders",
  "routing_key": "order.new"
}'

# Test wysyłania wiadomości
curl -X POST http://localhost:5672/orders -H "Content-Type: application/json" \
  -d '{"order_id": "123", "items": ["item1", "item2"]}'
```

### 7. Cache System

```bash
# Endpoint Redis cache
uripoint --uri redis://localhost:6379/cache --data '{
  "db": 0,
  "decode_responses": true
}'

# Test operacji cache
curl -X GET http://localhost:6379/cache/user:123
curl -X PUT http://localhost:6379/cache/user:123 -d '{"name": "John", "age": 30}'
```

### 8. Email Service

```bash
# Endpoint SMTP
uripoint --uri smtp://localhost:587/mail --data '{
  "use_tls": true,
  "timeout": 30
}'

# Test wysyłania maila
curl -X POST http://localhost:587/mail -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Test",
    "body": "Hello World"
  }'
```

### 9. DNS Service

```bash
# Endpoint DNS
uripoint --uri dns://localhost:53/lookup --data '{
  "timeout": 5,
  "cache_enabled": true
}'

# Test zapytań DNS
curl -X GET http://localhost:53/lookup?domain=example.com
```

### 10. WebSocket Chat

```bash
# Endpoint WebSocket
uripoint --uri ws://localhost:8080/chat --data '{
  "protocol": "chat",
  "max_connections": 100
}'

# Test połączenia WebSocket
wscat -c ws://localhost:8080/chat
```

### 11. Monitoring System

```bash
# Endpoint metryk
uripoint --uri http://localhost:9090/metrics --data '{
  "response": {
    "cpu_usage": 45,
    "memory_usage": 60,
    "disk_space": 80
  }
}' --method GET

# Test monitoringu
curl -X GET http://localhost:9090/metrics
```

### 12. File Storage

```bash
# Endpoint storage
uripoint --uri http://localhost:8000/storage --data '{
  "base_path": "/tmp/storage",
  "max_size": "100M"
}' --method GET POST DELETE

# Testy storage
curl -X POST http://localhost:8000/storage -F "file=@test.txt"
curl -X GET http://localhost:8000/storage/test.txt
curl -X DELETE http://localhost:8000/storage/test.txt
```

### 13. GraphQL API

```bash
# Endpoint GraphQL
uripoint --uri http://localhost:4000/graphql --data '{
  "schema": "type Query { users: [User] }",
  "resolvers": {"Query": {"users": []}}
}' --method POST

# Test GraphQL
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name } }"}'
```

### 14. Load Balancer

```bash
# Endpointy backend serwerów
uripoint --uri http://localhost:8001/api --data '{"response": {"server": "1"}}'
uripoint --uri http://localhost:8002/api --data '{"response": {"server": "2"}}'

# Test load balancera
curl -X GET http://localhost:8001/api
curl -X GET http://localhost:8002/api
```

### 15. Event Stream

```bash
# Endpoint SSE (Server-Sent Events)
uripoint --uri http://localhost:8000/events --data '{
  "response": {"type": "sse"},
  "headers": {"Content-Type": "text/event-stream"}
}'

# Test strumienia zdarzeń
curl -N http://localhost:8000/events
```

[Rest of previous content remains unchanged...]
