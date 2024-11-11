# UriPoint

## Overview

UriPoint is a flexible Python library for creating, managing, and interacting with network endpoints across multiple protocols. It provides a unified interface for handling various communication protocols, including streaming protocols (RTSP, HLS, DASH) and IoT protocols (MQTT).

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

## Protocol Examples

### Streaming Protocols

#### RTSP Example
```python
from uripoint import UriPointCLI

# Create RTSP endpoint for security camera
cli = UriPointCLI()
cli.create_endpoint(
    uri='rtsp://localhost:8554/camera1',
    data={
        'stream_url': 'rtsp://camera.example.com/stream1',
        'transport': 'tcp',
        'auth': {
            'username': 'admin',
            'password': 'secure123'
        }
    }
)
```

#### HLS Example
```python
# Create HLS endpoint for live streaming
cli.create_endpoint(
    uri='http://localhost:8080/live/stream.m3u8',
    data={
        'manifest_url': '/live/stream.m3u8',
        'segment_duration': 6,
        'options': {
            'bandwidth_variants': [
                {'resolution': '1080p', 'bitrate': 5000000},
                {'resolution': '720p', 'bitrate': 2500000}
            ]
        }
    }
)
```

#### DASH Example
```python
# Create DASH endpoint for video on demand
cli.create_endpoint(
    uri='http://localhost:8080/vod/manifest.mpd',
    data={
        'mpd_url': '/vod/manifest.mpd',
        'segment_duration': 4,
        'options': {
            'quality_levels': [
                {'resolution': '2160p', 'bitrate': 15000000},
                {'resolution': '1080p', 'bitrate': 4500000}
            ]
        }
    }
)
```

### IoT Protocols

#### MQTT Example
```python
# Create MQTT endpoint for temperature sensor
cli.create_endpoint(
    uri='mqtt://localhost:1883/sensors/temperature',
    data={
        'topic': 'sensors/temperature',
        'qos': 1,
        'retain': True,
        'device': {
            'id': 'temp_sensor_01',
            'type': 'temperature',
            'location': 'living_room'
        }
    }
)

# Create MQTT endpoint for smart light control
cli.create_endpoint(
    uri='mqtt://localhost:1883/devices/lights',
    data={
        'topic': 'devices/lights',
        'qos': 1,
        'retain': True,
        'device': {
            'id': 'smart_light_01',
            'capabilities': ['dimming', 'color']
        }
    }
)
```

See [examples/protocol_examples/](examples/protocol_examples/) for more comprehensive examples:
- [streaming_example.py](examples/protocol_examples/streaming_example.py): RTSP, HLS, and DASH streaming
- [mqtt_iot_example.py](examples/protocol_examples/mqtt_iot_example.py): IoT device communication
- [redis_example.py](examples/protocol_examples/redis_example.py): Data store access
- [smtp_example.py](examples/protocol_examples/smtp_example.py): Email handling
- [amqp_example.py](examples/protocol_examples/amqp_example.py): Message queuing
- [dns_example.py](examples/protocol_examples/dns_example.py): Domain resolution

## Supported Protocols

### Streaming Protocols
- RTSP
  - Security camera streams
  - Live video feeds
  - Transport options (TCP/UDP)
  - Authentication support

- HLS (HTTP Live Streaming)
  - Live streaming
  - Video on demand
  - Adaptive bitrate
  - Multiple quality variants

- DASH (Dynamic Adaptive Streaming over HTTP)
  - Video on demand
  - Live streaming
  - Multiple quality levels
  - Multi-language support

### IoT and Messaging Protocols
- MQTT
  - IoT device communication
  - QoS levels
  - Retain messages
  - Topic-based routing
  - Device management

### Web Protocols
- HTTP/HTTPS
  - RESTful API endpoints
  - Method-specific handling
  - CORS support
  - Static file serving

### Data Store Protocols
- Redis
  - Caching and data storage
  - Multiple database support
  - Key expiration

### Email Protocols
- SMTP
  - Email sending capabilities
  - HTML and plain text support
  - Template system
  - Attachments handling

### Message Queue Protocols
- AMQP (RabbitMQ)
  - Message queuing
  - Exchange types
  - Routing capabilities
  - Durable queues

### Domain Name Protocols
- DNS
  - Forward and reverse lookups
  - Multiple record types
  - DNS monitoring
  - Caching support

## Configuration File Location
- **Path**: `~/.uripoint_config.yaml`
- **Format**: YAML
- **Contents**: List of endpoint configurations

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License
This project is licensed under the terms of the LICENSE file in the project root.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
