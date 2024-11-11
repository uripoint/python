# UriPoint Endpoint Demonstration

## Overview
This example demonstrates creating and interacting with multiple service endpoints using UriPoint's flexible CLI.

## Endpoint Creation Methods

### 1. Full URI Method
```bash
# Create an endpoint using full URI
uripoint --uri http://localhost:8001/api/users --data '{"service": "user_management"}'
```

### 2. Component-Based Method
```bash
# Create an endpoint using individual components
uripoint --hostname localhost --path /api/users --protocol http --port 8001 --data '{"service": "user_management"}'
```

## Services and Testing

### User Management Service (Port 8001)
#### Create Endpoint
```bash
# Full URI Method
uripoint --uri http://localhost:8001/api/users

# Component-Based Method
uripoint --hostname localhost --path /api/users --protocol http --port 8001 --data '{"service": "user_management"}'
```

#### Test Commands
```bash
# List all users
curl http://localhost:8001/api/users

# Create a new user
curl -X POST http://localhost:8001/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com"}'

# Get a specific user
curl http://localhost:8001/api/users/1
```

### Product Catalog Service (Port 8002)
#### Create Endpoint
```bash
# Full URI Method
uripoint --uri http://localhost:8002/api/products

# Component-Based Method
uripoint --hostname localhost --path /api/products --protocol http --port 8002 --data '{"service": "product_catalog"}'
```

#### Test Commands
```bash
# List all products
curl http://localhost:8002/api/products

# Get a specific product
curl http://localhost:8002/api/products/1
```

### Order Processing Service (Port 8003)
#### Create Endpoint
```bash
# Full URI Method
uripoint --uri http://localhost:8003/api/orders

# Component-Based Method
uripoint --hostname localhost --path /api/orders --protocol http --port 8003 --data '{"service": "order_processing"}'
```

#### Test Commands
```bash
# List all orders
curl http://localhost:8003/api/orders

# Create a new order
curl -X POST http://localhost:8003/api/orders \
     -H "Content-Type: application/json" \
     -d '{"product_id": 1, "quantity": 2}'

# Get a specific order
curl http://localhost:8003/api/orders/1
```

## Endpoint Management

### List All Endpoints
```bash
uripoint --list
```

### Serve All Endpoints
```bash
uripoint --serve
```

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start all services:
```bash
./start_services.sh
```

3. Test services:
```bash
./test_services.sh
```

## Notes
- Ensure all services are running before testing
- Modify curl commands as needed based on your specific use case
- Check service logs for additional debugging information
