# UriPoint

## Overview

UriPoint is a flexible Python library for creating, managing, and interacting with network endpoints across multiple protocols.

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

## Installation

```bash
pip install uripoint
```

## CLI Usage

### Endpoint Creation Methods

1. Full URI Approach
```bash
# Create an endpoint with full URI
uripoint --uri http://localhost:8080/api/status --data '{"status": "OK"}'
```

2. Component-Based Approach
```bash
# Create an endpoint using individual components
uripoint --hostname localhost --path /api/status --protocol http --port 8001 --data '{"status": "OK"}'
```

### Endpoint Management

```bash
# List all configured endpoints
uripoint --list

# Serve all configured endpoints
uripoint --serve

uripoint --test
```

### Persistent Configuration

#### How Configuration Works
- Endpoints are saved in `~/.uripoint_config.yaml`
- Each endpoint includes:
  - Protocol
  - Hostname
  - Path
  - Port
  - Optional metadata

#### Example Workflow
```bash
# Create first endpoint
uripoint --hostname localhost --path /api/users --port 8001

# Create second endpoint
uripoint --hostname localhost --path /api/products --port 8002

# List all endpoints (persists between sessions)
uripoint --list

# Serve all endpoints
uripoint --serve
```

## Supported Protocols

### Web Protocols
- HTTP
- HTTPS
- WebSocket (WS)
- WebSocket Secure (WSS)

### File Transfer Protocols
- FTP
- SFTP

### IoT and Messaging Protocols
- MQTT
  - Supports IoT device communication
  - QoS levels and retain messages
  - Topic-based routing
  - See [MQTT Example](examples/protocol_examples/mqtt_example.py)

### Data Store Protocols
- Redis
  - Caching and data storage
  - Multiple database support
  - Key expiration
  - See [Redis Example](examples/protocol_examples/redis_example.py)

### Email Protocols
- SMTP
  - Email sending capabilities
  - HTML and plain text support
  - Template system
  - Attachments handling
  - See [SMTP Example](examples/protocol_examples/smtp_example.py)

### Message Queue Protocols
- AMQP (RabbitMQ)
  - Message queuing
  - Exchange types (direct, topic, fanout)
  - Routing capabilities
  - Durable queues
  - See [AMQP Example](examples/protocol_examples/amqp_example.py)

### Domain Name Protocols
- DNS
  - Forward and reverse lookups
  - Multiple record types (A, AAAA, MX, TXT, SRV)
  - DNS monitoring
  - Caching support
  - See [DNS Example](examples/protocol_examples/dns_example.py)

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

## Configuration File Location
- **Path**: `~/.uripoint_config.yaml`
- **Format**: YAML
- **Contents**: List of endpoint configurations

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License
This project is licensed under the terms of the LICENSE file in the project root.
