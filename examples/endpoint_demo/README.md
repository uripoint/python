# UriPoint Endpoint Demonstration

## Overview
This example demonstrates creating and interacting with multiple service endpoints using UriPoint.

## Services
1. User Management Service
2. Product Catalog Service
3. Order Processing Service

## Setup and Running

### Start Services
```bash
# Create endpoints using UriPoint
uripoint --uri /api/users --protocol http --port 8001 --data '{"service": "user_management"}'
uripoint --uri /api/products --protocol http --port 8002 --data '{"service": "product_catalog"}'
uripoint --uri /api/orders --protocol http --port 8003 --data '{"service": "order_processing"}'
```

### Test Endpoints
```bash
# User Management Service
curl http://localhost:8001/api/users
curl -X POST http://localhost:8001/api/users -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}'

# Product Catalog Service
curl http://localhost:8002/api/products
curl http://localhost:8002/api/products/1

# Order Processing Service
curl http://localhost:8003/api/orders
curl -X POST http://localhost:8003/api/orders -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 2}'
