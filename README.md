# UriPoint

## Overview

UriPoint is a flexible Python library for creating, managing, and interacting with network endpoints across multiple protocols. It provides a unified interface for handling various communication protocols and includes a built-in server for serving live endpoints with HTTP method support.

## Key Features

### Persistent Endpoint Management
UriPoint provides a robust CLI for creating and managing endpoints that persist across sessions.

#### How It Works
1. **Configuration Storage**
   - Endpoints are stored in `~/.uripoint_config.yaml`
   - Automatically saves and loads endpoint configurations
   - Maintains state between CLI sessions

2. **Endpoint Creation**
   - Supports multiple creation methods
   - Prevents duplicate endpoint registration
   - Stores endpoint details with associated metadata
   - Configurable HTTP methods

3. **Live Server**
   - Built-in HTTP server for serving endpoints
   - Multi-port support
   - Protocol-specific handlers
   - HTTP method validation
   - CORS support

## Installation

```bash
pip install uripoint
```

## CLI Usage

### Endpoint Creation Methods

1. Full URI Approach with HTTP Methods
```bash
# Create an endpoint with full URI and specific HTTP methods
uripoint --uri http://localhost:8080/api/users --data '{"response": {"status": "OK"}}' --method GET POST PUT
```

2. Component-Based Approach
```bash
# Create an endpoint using individual components
uripoint --hostname localhost --path /api/status --protocol http --port 8001 --data '{"status": "OK"}' --method GET
```

### Endpoint Management

```bash
# List all configured endpoints
uripoint --list

# Serve all endpoints as a live server
uripoint --serve

# Test endpoints
uripoint --test

# Detach specific endpoints
uripoint --detach "http://localhost:9000/api/hello" "http://localhost:9001/metrics"

# Detach all endpoints
uripoint --detach
```

### HTTP Method Configuration

Endpoints can be configured to accept specific HTTP methods:

```yaml
# Example endpoint configuration
endpoints:
  "http://localhost:9000/api/users":
    response:
      users: []
    content_type: "application/json"
    methods: ["GET", "POST", "PUT", "DELETE"]  # Allowed methods

  "http://localhost:9000/api/status":
    response:
      status: "OK"
    content_type: "application/json"
    methods: ["GET"]  # Read-only endpoint
```

### Server Example

Create test endpoints with method configuration:

```python
from uripoint import UriPointCLI

def setup_test_endpoints():
    cli = UriPointCLI()

    # Create a read-only endpoint
    cli.create_endpoint(
        uri='http://localhost:9000/api/status',
        data={
            'response': {'status': 'OK'},
            'methods': ['GET']
        }
    )

    # Create a full CRUD endpoint
    cli.create_endpoint(
        uri='http://localhost:9000/api/users',
        data={
            'response': {'users': []},
            'methods': ['GET', 'POST', 'PUT', 'DELETE']
        }
    )

setup_test_endpoints()
```

Then run the server:
```bash
# Start the server
uripoint --serve

# Test different methods
curl -X GET http://localhost:9000/api/users
curl -X POST http://localhost:9000/api/users -d '{"name": "John"}'
curl -X PUT http://localhost:9000/api/users/1 -d '{"name": "John Doe"}'
curl -X DELETE http://localhost:9000/api/users/1

# Check allowed methods
curl -X OPTIONS http://localhost:9000/api/users
```

## Supported Protocols

### Web Protocols
- HTTP/HTTPS
  - RESTful API endpoints
  - Method-specific handling (GET, POST, PUT, DELETE, etc.)
  - CORS support
  - Static file serving
  - Proxy support
  - See examples/endpoint_demo/

[Rest of protocol documentation remains unchanged...]

## Protocol Examples

Each protocol comes with a comprehensive example demonstrating its usage:

```python
# HTTP Example with Methods
from uripoint import UriPointCLI

def setup_http():
    cli = UriPointCLI()
    cli.create_endpoint(
        uri='http://localhost:9000/api/users',
        data={
            'response': {'users': []},
            'methods': ['GET', 'POST', 'PUT', 'DELETE']
        }
    )

[Rest of examples remain unchanged...]
```

## Configuration File Location
- **Path**: `~/.uripoint_config.yaml`
- **Format**: YAML
- **Contents**: List of endpoint configurations with method support

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License
This project is licensed under the terms of the LICENSE file in the project root.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
