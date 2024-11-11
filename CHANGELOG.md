# Changelog

## [1.2.0] - HTTP Method Support and Server Enhancements
### Added
- HTTP method configuration for endpoints
- Support for GET, POST, PUT, DELETE, PATCH, OPTIONS
- CORS headers for cross-origin requests
- Method-specific error handling
- Endpoint detachment functionality
- Enhanced server logging

### Implemented
- Method validation in endpoint configuration
- Selective endpoint detachment
- Multi-port server support
- Request method handling
- CORS support

### Improvements
- Better error messages for invalid methods
- Enhanced endpoint configuration
- Improved server logging
- More flexible endpoint management

## [1.1.0] - Protocol Expansion and Process Management
### Added
- New protocol implementations:
  - MQTT for IoT device communication
  - Redis for caching and data storage
  - SMTP for email handling
  - AMQP (RabbitMQ) for message queuing
  - DNS for domain resolution
- Comprehensive protocol examples in examples/protocol_examples/
- Enhanced process management with robust error handling

### Implemented
- Protocol-specific handlers with validation
- Example implementations for each new protocol
- Improved process management with proper argument handling
- Thread-safe operations in process management

### Improvements
- Enhanced error propagation in process management
- More robust protocol validation
- Expanded test coverage
- Updated documentation for new protocols

## [1.0.0] - Stable Release and Major Feature Consolidation
[Rest of changelog remains unchanged...]
