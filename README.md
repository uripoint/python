# UriPoint - Universal Network Endpoint Management

UriPoint is a comprehensive Python library designed for unified network endpoint management across multiple protocols. It simplifies the creation, management, and monitoring of network endpoints through a single, cohesive interface.

### Why UriPoint?
- **Unified Management**: Handle multiple protocols through one interface
- **Simplified Configuration**: Easy setup through CLI or Python API
- **Protocol Agnostic**: Support for web, streaming, IoT, and messaging protocols
- **Production Ready**: Built-in monitoring, testing, and persistence

## Key Features

### Core Capabilities
1. **Protocol Unification**
   - Single interface for all supported protocols
   - Consistent API across different endpoint types
   - Standardized configuration format

2. **Management Tools**
   - CLI-based endpoint management
   - Configuration persistence
   - Real-time monitoring
   - Comprehensive testing framework

3. **Enterprise Features**
   - High availability support
   - Load balancing capabilities
   - Security integrations
   - Logging and metrics

### Technical Highlights
- **Persistent Configuration**: YAML-based storage (`~/.uripoint_config.yaml`)
- **Protocol Handlers**: Dedicated handlers for each supported protocol
- **Monitoring System**: Real-time endpoint status tracking
- **Testing Suite**: Comprehensive testing framework with chaos engineering support

## Target Audience

### 1. Distributed Systems Developers
- Building microservices architectures
- Managing service discovery
- Implementing API gateways
- Developing service meshes

### 2. DevOps Engineers
- Infrastructure automation
- Service deployment
- Monitoring setup
- Configuration management

### 3. IoT Specialists
- Device management
- Sensor networks
- Data collection systems
- Remote monitoring

### 4. Streaming Engineers
- Video streaming services
- Live broadcast systems
- Security camera networks
- Content delivery networks

### 5. Backend Developers
- API development
- Service integration
- Message queue implementation
- Cache management

## Architecture

### System Components
```ascii
┌───────────────────────────────────────────────────────┐
│                    UriPoint System                    │
├───────────────┬──────────────────┬────────────────────┤
│ Core Engine   │ Protocol Layer   │ Management Layer   │
├───────────────┼──────────────────┼────────────────────┤
│ - Config      │ - HTTP/HTTPS     │ - CLI Interface    │
│ - Persistence │ - MQTT           │ - API Interface    │
│ - Monitoring  │ - RTSP           │ - Web Dashboard    │
│ - Testing     │ - Redis          │ - Monitoring UI    │
└───────────────┴──────────────────┴────────────────────┘
```

### Component Interaction
1. **Core Engine**
   - Configuration management
   - State persistence
   - Event handling
   - Resource management

2. **Protocol Layer**
   - Protocol-specific handlers
   - Data transformation
   - Connection management
   - Error handling

3. **Management Layer**
   - User interfaces
   - Monitoring tools
   - Administration features
   - Reporting systems

## Protocol Support

### Web & API Protocols
- **HTTP/HTTPS**
  - RESTful endpoints
  - WebHooks
  - Static content
  - API proxying

- **WebSocket**
  - Real-time communication
  - Bi-directional data flow
  - Connection pooling
  - Event streaming

### Streaming Protocols
- **RTSP**
  - Camera streams
  - Media servers
  - Stream recording
  - Transport selection

- **HLS/DASH**
  - Adaptive bitrate
  - Multi-quality
  - Live streaming
  - VOD support

### IoT & Messaging
- **MQTT**
  - Device management
  - Sensor data
  - Command control
  - State synchronization

- **AMQP**
  - Message queuing
  - Event routing
  - Dead letter handling
  - Queue management

## Installation & Setup

### Basic Installation
```bash
pip install uripoint
```

### Configuration
```yaml
# ~/.uripoint_config.yaml
endpoints:
  - name: api-endpoint
    uri: http://localhost:8080/api
    protocol: http
    methods: [GET, POST]
    
  - name: mqtt-sensor
    uri: mqtt://broker:1883/sensors
    protocol: mqtt
    qos: 1
```

## Usage Guide

### Service Lifecycle
```ascii
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│    Create    │   │  Configure   │   │    Deploy    │
│   Endpoint   ├──►│   Protocol   ├──►│   Service    │
└──────────────┘   └──────────────┘   └──────────────┘
       ▲                                      │
       │                                      ▼
┌──────────────┐                    ┌──────────────┐
│    Update    │◄───────────────────│   Monitor    │
│ Configuration│                    │    Status    │
└──────────────┘                    └──────────────┘
```

### CLI Commands


```bash
uripoint [options] <command>
```
```bash
┌────────────────────────────────────────────────┐
│ --uri      Define endpoint URI                 │
│ --method   Specify HTTP methods                │
│ --data     Configure endpoint data             │
│ --serve    Start serving endpoints             │
│ --list     Show configured endpoints           │
│ --detach   Remove endpoints                    │
└────────────────────────────────────────────────┘
```

### Endpoint Management
Options
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

Examples
```bash
uripoint create --uri http://localhost:8080/api --protocol http
uripoint list [--format json|yaml]
uripoint serve [--port 8000]
uripoint monitor [--interval 5]
uripoint remove [endpoint-name]
```

Protocol-Specific Commands
```bash
uripoint stream start --uri rtsp://camera:554/feed
uripoint mqtt publish --topic sensors/temp --message "23.5"
uripoint http test --endpoint api-endpoint
```

High Availability Setup
```python
from uripoint import HighAvailability

ha = HighAvailability(
    endpoints=['endpoint1', 'endpoint2'],
    strategy='active-passive',
    failover_timeout=30
)
ha.start()
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


# UriPoint Implementation Examples

## Table of Contents
1. [Web API Examples](#web-api-examples)
2. [Streaming Examples](#streaming-examples)
3. [IoT Examples](#iot-examples)
4. [Message Queue Examples](#message-queue-examples)
5. [Storage Examples](#storage-examples)
6. [Email Examples](#email-examples)
7. [Multi-Protocol Examples](#multi-protocol-examples)

## Web API Examples

### 1. Basic REST API Endpoint

```bash
# CLI Command
uripoint --uri http://localhost:8080/api/users \
         --method GET POST PUT DELETE \
         --data '{
           "response": {"users": []},
           "cors": true,
           "auth": {"type": "basic"}
         }'

# Test Commands
curl -X GET http://localhost:8080/api/users
curl -X POST http://localhost:8080/api/users -d '{"name": "John"}'
curl -X PUT http://localhost:8080/api/users/1 -d '{"name": "John Doe"}'
curl -X DELETE http://localhost:8080/api/users/1

# Verification
uripoint --test http://localhost:8080/api/users --method GET
uripoint --verify http://localhost:8080/api/users
```

```python
# Python Implementation
from uripoint import UriPointCLI, EndpointTest

# Create endpoint
cli = UriPointCLI()
endpoint = cli.create_endpoint(
    uri='http://localhost:8080/api/users',
    data={
        'response': {'users': []},
        'methods': ['GET', 'POST', 'PUT', 'DELETE'],
        'cors': True,
        'auth': {'type': 'basic'}
    }
)

# Test endpoint
test = EndpointTest(endpoint)
test.run_http_tests()
test.verify_cors()
test.check_methods()
```

## Streaming Examples

### 2. RTSP Camera Stream

```bash
# CLI Command
uripoint --uri rtsp://localhost:8554/camera1 \
         --data '{
           "stream_url": "rtsp://camera.example.com/stream1",
           "transport": "tcp",
           "authentication": {
             "username": "${CAMERA_USER}",
             "password": "${CAMERA_PASS}"
           },
           "options": {
             "framerate": 30,
             "resolution": "1920x1080"
           }
         }'

# Test Commands
ffplay rtsp://localhost:8554/camera1
ffprobe -v error -show_entries stream=codec_type rtsp://localhost:8554/camera1

# Verification
uripoint --test rtsp://localhost:8554/camera1 --check-stream
uripoint --verify rtsp://localhost:8554/camera1 --params framerate,resolution
```

```python
# Python Implementation
from uripoint import UriPointCLI, StreamTest

# Create streaming endpoint
cli = UriPointCLI()
stream = cli.create_stream_endpoint(
    uri='rtsp://localhost:8554/camera1',
    data={
        'stream_url': 'rtsp://camera.example.com/stream1',
        'transport': 'tcp',
        'authentication': {
            'username': os.getenv('CAMERA_USER'),
            'password': os.getenv('CAMERA_PASS')
        },
        'options': {
            'framerate': 30,
            'resolution': '1920x1080'
        }
    }
)

# Test stream
test = StreamTest(stream)
test.verify_stream_health()
test.check_parameters()
test.monitor_bandwidth()
```

## IoT Examples

### 3. MQTT Temperature Sensor Network

```bash
# CLI Command
uripoint --uri mqtt://localhost:1883/sensors/temperature \
         --data '{
           "topics": ["sensors/+/temperature"],
           "qos": 1,
           "retain": true,
           "device_schema": {
             "type": "temperature",
             "unit": "celsius",
             "interval": 60
           }
         }'

# Test Commands
mosquitto_pub -h localhost -t sensors/room1/temperature -m '{"value": 22.5}'
mosquitto_sub -h localhost -t 'sensors/+/temperature'

# Verification
uripoint --test mqtt://localhost:1883/sensors/temperature
uripoint --verify mqtt://localhost:1883/sensors/temperature --check-schema
```

```python
# Python Implementation
from uripoint import UriPointCLI, MQTTTest

# Create MQTT endpoint
cli = UriPointCLI()
mqtt = cli.create_mqtt_endpoint(
    uri='mqtt://localhost:1883/sensors/temperature',
    data={
        'topics': ['sensors/+/temperature'],
        'qos': 1,
        'retain': True,
        'device_schema': {
            'type': 'temperature',
            'unit': 'celsius',
            'interval': 60
        }
    }
)

# Test MQTT endpoint
test = MQTTTest(mqtt)
test.verify_connectivity()
test.test_pub_sub()
test.validate_messages()
```

## Message Queue Examples

### 4. AMQP Order Processing Queue

```bash
# CLI Command
uripoint --uri amqp://localhost:5672/orders \
         --data '{
           "exchange": "order_exchange",
           "queues": {
             "new_orders": {"durable": true},
             "processed_orders": {"durable": true}
           },
           "routing_keys": ["order.new", "order.processed"],
           "dlx": "order_dlx"
         }'

# Test Commands
curl -X POST http://localhost:5672/orders/send \
     -d '{"order_id": "123", "status": "new"}'
curl -X GET http://localhost:5672/orders/status

# Verification
uripoint --test amqp://localhost:5672/orders --check-queues
uripoint --verify amqp://localhost:5672/orders --check-bindings
```

```python
# Python Implementation
from uripoint import UriPointCLI, AMQPTest

# Create AMQP endpoint
cli = UriPointCLI()
amqp = cli.create_amqp_endpoint(
    uri='amqp://localhost:5672/orders',
    data={
        'exchange': 'order_exchange',
        'queues': {
            'new_orders': {'durable': True},
            'processed_orders': {'durable': True}
        },
        'routing_keys': ['order.new', 'order.processed'],
        'dlx': 'order_dlx'
    }
)

# Test AMQP endpoint
test = AMQPTest(amqp)
test.verify_exchange()
test.check_queues()
test.test_message_flow()
```

## Storage Examples

### 5. Redis Cache System

```bash
# CLI Command
uripoint --uri redis://localhost:6379/cache \
         --data '{
           "database": 0,
           "key_prefix": "app:",
           "max_connections": 10,
           "timeout": 5,
           "encoding": "utf-8"
         }'

# Test Commands
curl -X SET http://localhost:6379/cache/user:123 -d '{"name": "John"}'
curl -X GET http://localhost:6379/cache/user:123
redis-cli -h localhost PING

# Verification
uripoint --test redis://localhost:6379/cache --check-connection
uripoint --verify redis://localhost:6379/cache --check-encoding
```

```python
# Python Implementation
from uripoint import UriPointCLI, RedisTest

# Create Redis endpoint
cli = UriPointCLI()
redis = cli.create_redis_endpoint(
    uri='redis://localhost:6379/cache',
    data={
        'database': 0,
        'key_prefix': 'app:',
        'max_connections': 10,
        'timeout': 5,
        'encoding': 'utf-8'
    }
)

# Test Redis endpoint
test = RedisTest(redis)
test.verify_connectivity()
test.test_operations()
test.check_performance()
```

## Email Examples

### 6. SMTP Email Service

```bash
# CLI Command
uripoint --uri smtp://smtp.gmail.com:587/mail \
         --data '{
           "auth": {
             "username": "${SMTP_USER}",
             "password": "${SMTP_PASS}"
           },
           "tls": true,
           "templates": {
             "welcome": {"path": "templates/welcome.html"},
             "reset": {"path": "templates/reset.html"}
           }
         }'

# Test Commands
curl -X POST http://localhost:587/mail/send \
     -d '{
       "to": "user@example.com",
       "template": "welcome",
       "data": {"name": "John"}
     }'

# Verification
uripoint --test smtp://smtp.gmail.com:587/mail --check-auth
uripoint --verify smtp://smtp.gmail.com:587/mail --check-templates
```

```python
# Python Implementation
from uripoint import UriPointCLI, SMTPTest

# Create SMTP endpoint
cli = UriPointCLI()
smtp = cli.create_smtp_endpoint(
    uri='smtp://smtp.gmail.com:587/mail',
    data={
        'auth': {
            'username': os.getenv('SMTP_USER'),
            'password': os.getenv('SMTP_PASS')
        },
        'tls': True,
        'templates': {
            'welcome': {'path': 'templates/welcome.html'},
            'reset': {'path': 'templates/reset.html'}
        }
    }
)

# Test SMTP endpoint
test = SMTPTest(smtp)
test.verify_connection()
test.test_templates()
test.check_delivery()
```

## Multi-Protocol Examples

### 7. Full IoT Monitoring System

```bash
# CLI Commands
# Create MQTT endpoint for sensor data
uripoint --uri mqtt://localhost:1883/sensors \
         --data '{
           "topics": ["sensors/#"],
           "qos": 1
         }'

# Create Redis endpoint for data storage
uripoint --uri redis://localhost:6379/sensor-data \
         --data '{
           "database": 1,
           "expire": 3600
         }'

# Create HTTP API endpoint
uripoint --uri http://localhost:8080/api/sensors \
         --method GET POST \
         --data '{
           "cache": "redis://localhost:6379/sensor-data",
           "mqtt": "mqtt://localhost:1883/sensors"
         }'

# Test Commands
# Test MQTT data flow
mosquitto_pub -t sensors/temp1 -m '{"value": 24.5}'

# Check Redis storage
redis-cli -h localhost -n 1 GET sensor:temp1

# Verify HTTP API
curl http://localhost:8080/api/sensors/temp1

# Verification
uripoint --test-suite iot-monitoring --verify-all
```

```python
# Python Implementation
from uripoint import UriPointCLI, SystemTest

# Create system endpoints
cli = UriPointCLI()

# MQTT endpoint
mqtt = cli.create_mqtt_endpoint(
    uri='mqtt://localhost:1883/sensors',
    data={
        'topics': ['sensors/#'],
        'qos': 1
    }
)

# Redis endpoint
redis = cli.create_redis_endpoint(
    uri='redis://localhost:6379/sensor-data',
    data={
        'database': 1,
        'expire': 3600
    }
)

# HTTP API endpoint
api = cli.create_endpoint(
    uri='http://localhost:8080/api/sensors',
    data={
        'methods': ['GET', 'POST'],
        'cache': 'redis://localhost:6379/sensor-data',
        'mqtt': 'mqtt://localhost:1883/sensors'
    }
)

# Create system test
test = SystemTest([mqtt, redis, api])
test.verify_integration()
test.test_data_flow()
test.check_performance()
```

## Testing Framework Examples

### Common Test Cases

```python
# Basic endpoint test
test = EndpointTest(endpoint)
test.run()

# Protocol-specific tests
test.verify_protocol()
test.check_security()
test.validate_performance()

# Integration tests
test.verify_dependencies()
test.check_data_flow()
test.test_failover()

# Load tests
test.concurrent_access(num_clients=100)
test.sustained_load(duration=300)
test.peak_performance()

# Chaos tests
test.network_partition()
test.process_failure()
test.data_corruption()
```

### Test Configuration

```yaml
# test_config.yaml
tests:
  performance:
    concurrent_users: 100
    duration: 300
    thresholds:
      latency_p95: 200
      error_rate: 0.01
  
  integration:
    dependencies:
      - redis
      - mqtt
      - http
    timeout: 30
    
  chaos:
    scenarios:
      - network_partition
      - process_crash
      - disk_full
    duration: 600
```


See [examples/protocol_examples/](examples/protocol_examples/) for more comprehensive examples:
- [streaming_example.py](examples/protocol_examples/streaming_example.py): RTSP, HLS, and DASH streaming
- [mqtt_iot_example.py](examples/protocol_examples/mqtt_iot_example.py): IoT device communication
- [redis_example.py](examples/protocol_examples/redis_example.py): Data store access
- [smtp_example.py](examples/protocol_examples/smtp_example.py): Email handling
- [amqp_example.py](examples/protocol_examples/amqp_example.py): Message queuing
- [dns_example.py](examples/protocol_examples/dns_example.py): Domain resolution


## Configuration File Location
- **Path**: `~/.uripoint_config.yaml`
- **Format**: YAML
- **Contents**: List of endpoint configurations




## Testing Framework

UriPoint includes a comprehensive testing framework that ensures reliability and performance across all components:

```ascii
┌────────────────────────┐  ┌─────────────────────────┐
│   Performance Tests    │  │   Integration Tests     │
├────────────────────────┤  ├─────────────────────────┤
│ - Endpoint Creation    │  │ - Component Interaction │
│ - Concurrent Access    │  │ - Multi-Protocol        │
│ - Memory Usage         │  │ - Process Management    │
│ - Protocol Handlers    │  │ - Error Propagation     │
└────────────────────────┘  └─────────────────────────┘

┌────────────────────────┐  ┌─────────────────────────┐
│     Chaos Tests        │  │    Protocol Tests       │
├────────────────────────┤  ├─────────────────────────┤
│ - Random Operations    │  │ - Protocol Validation   │
│ - Process Chaos        │  │ - Handler Behavior      │
│ - Network Simulation   │  │ - Configuration         │
│ - Data Input Chaos     │  │ - Error Handling        │
└────────────────────────┘  └─────────────────────────┘
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_protocols.py
pytest tests/test_performance.py
pytest tests/test_integration.py
pytest tests/test_chaos.py

# Run with coverage report
pytest --cov=uripoint tests/
```

### Test Categories

1. **Performance Tests**
   - Endpoint creation benchmarks
   - Concurrent access testing
   - Memory usage monitoring
   - Protocol handler performance

2. **Integration Tests**
   - Component interaction verification
   - Multi-protocol integration
   - Process-endpoint integration
   - Error propagation testing

3. **Chaos Tests**
   - Random endpoint operations
   - Process management chaos
   - Network chaos simulation
   - Data input chaos testing

4. **Protocol-Specific Tests**
   - Protocol handler validation
   - Configuration verification
   - Error handling
   - Protocol behavior testing



## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License
This project is licensed under the terms of the LICENSE file in the project root.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history and updates.



## Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details on:
- Code style
- Pull request process
- Development setup
- Testing requirements

## Support

- **Support**: Community support via GitHub Issues
- **Documentation**: Full docs at [docs.uripoint.com](https://docs.uripoint.com)
- **Updates**: See [CHANGELOG.md](CHANGELOG.md)