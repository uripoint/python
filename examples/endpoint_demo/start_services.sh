#!/bin/bash

# Ensure executable
chmod +x start_services.sh
chmod +x test_services.sh

# Start UriPoint endpoints
uripoint --uri /api/users --protocol http --port 8001 --data '{"service": "user_management"}'
uripoint --uri /api/products --protocol http --port 8002 --data '{"service": "product_catalog"}'
uripoint --uri /api/orders --protocol http --port 8003 --data '{"service": "order_processing"}'

# Start individual services in background
python user_service.py &
python product_service.py &
python order_service.py &

# Wait for all background processes
wait
