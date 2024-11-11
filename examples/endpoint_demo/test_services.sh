#!/bin/bash

echo "Testing User Management Service:"
curl http://localhost:8000/api/status
curl http://localhost:8001/api/users
echo -e "\n\nCreating a new user:"
curl -X POST http://localhost:8001/api/users -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}'

echo -e "\n\nTesting Product Catalog Service:"
curl http://localhost:8002/api/products
echo -e "\n\nFetching specific product:"
curl http://localhost:8002/api/products/1

echo -e "\n\nTesting Order Processing Service:"
curl http://localhost:8003/api/orders
echo -e "\n\nCreating a new order:"
curl -X POST http://localhost:8003/api/orders -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 2}'
