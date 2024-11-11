# UriPoint

## Overview

UriPoint is a comprehensive Python library for creating and managing endpoints across multiple protocols. It provides a flexible and powerful solution for setting up various network services with ease.

## Features

### Supported Protocols
- HTTP
- FTP
- RTSP (Real Time Streaming Protocol)
- MQTT (Message Queuing Telemetry Transport)
- WebSocket
- TCP
- UDP
- SMTP
- POP3
- SFTP

## Installation

```bash
pip install uripoint
```

## Quick Start

### Creating Endpoints

1. HTTP Endpoint
```bash
python uripoint.py --uri /api/status --protocol http --port 8000 --data '{"status": "OK"}'
```

2. FTP Server
```bash
python uripoint.py --uri /files --protocol ftp --port 2121 --data '{"directory": "./files"}'
```

3. RTSP Stream
```bash
python uripoint.py --uri /stream --protocol rtsp --port 8554 --data '{"stream_name": "test"}'
```

4. MQTT Broker
```bash
python uripoint.py --uri /mqtt --protocol mqtt --port 1883 --data '{"topics": ["test/#"]}'
```

### Additional Commands

- Run all servers:
```bash
python uripoint.py --serve
```

- List all endpoints:
```bash
python uripoint.py --list
```

## Key Capabilities

- Dynamic endpoint creation
- Multi-protocol support
- Persistent configuration (YAML-based)
- Flexible data handling
- Easy configuration and management

## Requirements

- Python 3.7+
- See `requirements.txt` for full dependencies

## Testing

To run tests:

```bash
python -m pytest
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## License

This project is licensed under the terms of the LICENSE file in the project root.

## Advanced Usage

Each endpoint is highly configurable and can handle various data types. The configuration is saved to a YAML file, ensuring endpoints persist between runs.

## Example Python Usage

```python
from uripoint import create_endpoint

# Create an HTTP endpoint
endpoint = create_endpoint(
    uri='/api/example',
    protocol='http',
    port=8000,
    data={'key': 'value'}
)
endpoint.start()
```

## Future Roadmap

- Enhanced protocol support
- Advanced routing mechanisms
- Improved security features
- More comprehensive documentation
