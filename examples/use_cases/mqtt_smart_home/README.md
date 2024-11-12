# MQTT Smart Home Monitoring System

## Why is this interesting?

MQTT is particularly interesting for smart home applications because:

1. **Lightweight Protocol**: MQTT's minimal overhead makes it perfect for IoT devices with limited resources
2. **Pub/Sub Pattern**: The publish/subscribe pattern allows multiple devices to communicate efficiently
3. **QoS Levels**: Different quality of service levels ensure reliable message delivery when needed
4. **Retained Messages**: New subscribers can immediately receive the last known state
5. **Topic Hierarchy**: Enables logical organization of different device types and rooms

## Use Case Description

This example implements a smart home monitoring system with:
- Temperature sensors in different rooms
- Motion detectors
- Light control
- Energy consumption monitoring

## Components

1. `app.py` - Main application that sets up MQTT endpoints and simulates devices
2. `Dockerfile` - Container configuration for the application
3. `docker-compose.yml` - Multi-container setup with MQTT broker and application

## Running the Example

1. Start the containers:
```bash
docker-compose up -d
```

2. Monitor the output:
```bash
docker-compose logs -f app
```

3. Stop the system:
```bash
docker-compose down
```

## URI Endpoints

- `mqtt://broker:1883/home/temperature/{room}` - Temperature readings
- `mqtt://broker:1883/home/motion/{location}` - Motion detection events
- `mqtt://broker:1883/home/lights/{room}` - Light control
- `mqtt://broker:1883/home/energy` - Energy consumption metrics
