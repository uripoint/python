# UriPoint

## Overview

UriPoint is a flexible Python library for creating, managing, and interacting with network endpoints across multiple protocols.

## Features

### Endpoint Management
- Create endpoints using full URI or component-based approach
- Support for multiple protocols (HTTP, HTTPS, WebSocket, FTP, etc.)
- Persistent endpoint configuration
- Easy endpoint listing and serving

## Installation

```bash
pip install uripoint
```

## CLI Usage

### Creating Endpoints

1. Full URI Approach
```bash
# Create an endpoint with full URI
uripoint --uri http://localhost:8080/api/status --data '{"status": "OK"}'
```

2. Component-Based Approach
```bash
# Create an endpoint using individual components
uripoint --hostname localhost --path /api/status --protocol http --port 8000 --data '{"status": "OK"}'
```

### Managing Endpoints

```bash
# List all configured endpoints
uripoint --list

# Serve all configured endpoints
uripoint --serve
```

## Example Scenarios

### HTTP Endpoint
```bash
# Create a simple HTTP status endpoint
uripoint --uri http://localhost:8000/health --data '{"status": "healthy"}'
```

### WebSocket Endpoint
```bash
# Create a WebSocket endpoint
uripoint --protocol ws --hostname localhost --path /socket --port 8765 --data '{"type": "websocket"}'
```

### FTP Endpoint
```bash
# Create an FTP endpoint
uripoint --protocol ftp --hostname ftp.example.com --path /files --port 21 --data '{"directory": "/public"}'
```

## Programmatic Usage

```python
from uripoint import UriPointCLI

# Create CLI instance
cli = UriPointCLI()

# Create an endpoint
cli.create_endpoint(
    uri='http://localhost:8000/api/status',
    data='{"status": "OK"}'
)

# List endpoints
cli.list_endpoints()

# Serve endpoints
cli.serve()
```

## Supported Protocols
- HTTP
- HTTPS
- WebSocket (WS)
- WebSocket Secure (WSS)
- FTP
- SFTP

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License
This project is licensed under the terms of the LICENSE file in the project root.
