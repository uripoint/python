# UriPoint

UriPoint is a flexible Python library for creating, managing, and interacting with network endpoints across multiple protocols. It provides a unified interface for handling various communication protocols, including streaming protocols (RTSP, HLS, DASH) and IoT protocols (MQTT).


```ascii
┌─────────────────────────────────────────────────────────────┐
│                      UriPoint System                        │
├──────────────────┬───────────────────┬──────────────────────┤
│   CLI Interface  │ Protocol Handlers │   Endpoint Manager   │
├──────────────────┴───────────────────┴──────────────────────┤
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐        │
│  │   HTTP(S)   │   │    MQTT     │   │    RTSP     │        │
│  │  Endpoints  │   │  Endpoints  │   │  Endpoints  │        │
│  └─────────────┘   └─────────────┘   └─────────────┘        │
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐        │
│  │   Redis     │   │    SMTP     │   │    AMQP     │        │
│  │  Endpoints  │   │  Endpoints  │   │  Endpoints  │        │
│  └─────────────┘   └─────────────┘   └─────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```


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


## Protocol Support

```ascii
┌─────────────────────────┐  ┌─────────────────────────┐
│     Web Protocols       │  │    Streaming Protocols  │
├─────────────────────────┤  ├─────────────────────────┤
│ - HTTP/HTTPS            │  │ - RTSP                  │
│ - WebSocket (WS/WSS)    │  │ - HLS                   │
│ - GraphQL               │  │ - DASH                  │
└─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐  ┌─────────────────────────┐
│    Storage Protocols    │  │   Messaging Protocols   │
├─────────────────────────┤  ├─────────────────────────┤
│ - Redis                 │  │ - MQTT                  │
│ - FTP/SFTP              │  │ - AMQP                  │
│ - File System           │  │ - SMTP                  │
└─────────────────────────┘  └─────────────────────────┘

 . . . & more
```


## Installation

```bash
pip install uripoint
```

## Usage


Service Life Cycle

```ascii
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Create    │     │   Configure │     │    Serve    │
│  Endpoint   │ ──► │   Protocol  │ ──► │  Endpoint   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                       │
       │                                       │
       ▼                                       ▼
┌─────────────┐                         ┌─────────────┐
│    Test     │ ◄─────────────────────  │   Monitor   │
│  Endpoint   │                         │   Status    │
└─────────────┘                         └─────────────┘
```

## Command

```bash
uripoint [options] <command>
```

Command
```bash
┌────────────────────────────────────────────────────┐
│ --uri      Define endpoint URI                     │
│ --method   Specify HTTP methods                    │
│ --data     Configure endpoint data                 │
│ --serve    Start serving endpoints                 │
│ --list     Show configured endpoints               │
│ --detach   Remove endpoints                        │
└────────────────────────────────────────────────────┘
```


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

### HTTP/REST API

```python
# Python
from uripoint import UriPointCLI

cli = UriPointCLI()
cli.create_endpoint(
    uri='http://localhost:8000/api/users',
    data={
        'response': {'users': []},
        'methods': ['GET', 'POST', 'PUT', 'DELETE']
    }
)
```

```bash
# CLI & curl
# Create endpoint
uripoint --uri http://localhost:8000/api/users --data '{"response": {"users": []}}' --method GET POST PUT DELETE

# Test endpoint
curl -X GET http://localhost:8000/api/users
curl -X POST http://localhost:8000/api/users -H "Content-Type: application/json" -d '{"name": "John"}'
curl -X PUT http://localhost:8000/api/users/1 -H "Content-Type: application/json" -d '{"name": "John Doe"}'
curl -X DELETE http://localhost:8000/api/users/1
```

### MQTT IoT Device

```python
# Python
cli.create_endpoint(
    uri='mqtt://localhost:1883/sensors/temperature',
    data={
        'topic': 'sensors/temperature',
        'qos': 1,
        'device': {
            'type': 'temperature',
            'location': 'room1'
        }
    }
)
```

```bash
# CLI & curl/mosquitto
# Create endpoint
uripoint --uri mqtt://localhost:1883/sensors/temperature --data '{"topic": "sensors/temperature", "qos": 1}'

# Test endpoint
mosquitto_pub -h localhost -p 1883 -t sensors/temperature -m '{"value": 22.5}'
mosquitto_sub -h localhost -p 1883 -t sensors/temperature
```

### Redis Cache

```python
# Python
cli.create_endpoint(
    uri='redis://localhost:6379/cache',
    data={
        'db': 0,
        'decode_responses': True,
        'max_connections': 10
    }
)
```

```bash
# CLI & curl
# Create endpoint
uripoint --uri redis://localhost:6379/cache --data '{"db": 0, "decode_responses": true}'

# Test endpoint
curl -X GET http://localhost:6379/cache/user:123
curl -X PUT http://localhost:6379/cache/user:123 -d '{"name": "John", "age": 30}'
curl -X DELETE http://localhost:6379/cache/user:123
```

### SMTP Email

```python
# Python
cli.create_endpoint(
    uri='smtp://smtp.gmail.com:587/mail',
    data={
        'use_tls': True,
        'timeout': 30
    }
)
```

```bash
# CLI & curl
# Create endpoint
uripoint --uri smtp://smtp.gmail.com:587/mail --data '{"use_tls": true, "timeout": 30}'

# Test endpoint
curl -X POST http://localhost:587/mail \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Test Email",
    "body": "Hello from UriPoint"
  }'
```

### RTSP Stream

```python
# Python
cli.create_endpoint(
    uri='rtsp://localhost:8554/camera1',
    data={
        'stream_url': 'rtsp://camera.example.com/stream1',
        'transport': 'tcp'
    }
)
```

```bash
# CLI & ffmpeg/curl
# Create endpoint
uripoint --uri rtsp://localhost:8554/camera1 --data '{"stream_url": "rtsp://camera.example.com/stream1", "transport": "tcp"}'

# Test endpoint
ffplay rtsp://localhost:8554/camera1
curl http://localhost:8554/camera1/info  # Get stream info
```

### HLS Stream

```python
# Python
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

```bash
# CLI & curl/ffmpeg
# Create endpoint
uripoint --uri http://localhost:8080/live/stream.m3u8 --data '{"manifest_url": "/live/stream.m3u8", "segment_duration": 6}'

# Test endpoint
curl http://localhost:8080/live/stream.m3u8  # Get manifest
ffplay http://localhost:8080/live/stream.m3u8  # Play stream
```



### DASH Example
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


### MQTT Example
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


### AMQP Message Queue

```python
# Python
cli.create_endpoint(
    uri='amqp://localhost:5672/orders',
    data={
        'exchange': 'orders',
        'queue': 'new_orders',
        'routing_key': 'order.new'
    }
)
```

```bash
# CLI & curl
# Create endpoint
uripoint --uri amqp://localhost:5672/orders --data '{"exchange": "orders", "queue": "new_orders"}'

# Test endpoint
curl -X POST http://localhost:5672/orders \
  -H "Content-Type: application/json" \
  -d '{"order_id": "123", "items": ["item1", "item2"]}'

curl -X GET http://localhost:5672/orders/status
```

### DNS Service

```python
# Python
cli.create_endpoint(
    uri='dns://localhost:53/lookup',
    data={
        'timeout': 5,
        'cache_enabled': True
    }
)
```

```bash
# CLI & curl/dig
# Create endpoint
uripoint --uri dns://localhost:53/lookup --data '{"timeout": 5, "cache_enabled": true}'

# Test endpoint
curl "http://localhost:53/lookup?domain=example.com"
dig @localhost example.com
```

### WebSocket Chat

```python
# Python
cli.create_endpoint(
    uri='ws://localhost:8080/chat',
    data={
        'protocol': 'chat',
        'max_connections': 100
    }
)
```

```bash
# CLI & websocat
# Create endpoint
uripoint --uri ws://localhost:8080/chat --data '{"protocol": "chat", "max_connections": 100}'

# Test endpoint
websocat ws://localhost:8080/chat
wscat -c ws://localhost:8080/chat
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


