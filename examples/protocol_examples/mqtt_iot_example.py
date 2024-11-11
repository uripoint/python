"""
Example demonstrating MQTT protocol with IoT devices
"""
from uripoint import UriPointCLI

def setup_mqtt_endpoints():
    cli = UriPointCLI()

    # Temperature sensor endpoint
    cli.create_endpoint(
        uri='mqtt://localhost:1883/sensors/temperature',
        data={
            'topic': 'sensors/temperature',
            'qos': 1,
            'retain': True,
            'device': {
                'id': 'temp_sensor_01',
                'type': 'temperature',
                'location': 'living_room',
                'update_interval': 60
            },
            'schema': {
                'temperature': 'float',
                'humidity': 'float',
                'battery': 'int',
                'timestamp': 'string'
            }
        }
    )

    # Motion sensor endpoint
    cli.create_endpoint(
        uri='mqtt://localhost:1883/sensors/motion',
        data={
            'topic': 'sensors/motion',
            'qos': 2,
            'retain': False,
            'device': {
                'id': 'motion_sensor_01',
                'type': 'motion',
                'location': 'entrance',
                'sensitivity': 'high'
            },
            'schema': {
                'motion_detected': 'boolean',
                'light_level': 'int',
                'battery': 'int',
                'timestamp': 'string'
            }
        }
    )

    # Smart light control endpoint
    cli.create_endpoint(
        uri='mqtt://localhost:1883/devices/lights',
        data={
            'topic': 'devices/lights',
            'qos': 1,
            'retain': True,
            'device': {
                'id': 'smart_light_01',
                'type': 'light',
                'location': 'living_room',
                'capabilities': ['dimming', 'color']
            },
            'schema': {
                'state': 'boolean',
                'brightness': 'int',
                'color': 'string',
                'power_usage': 'float',
                'timestamp': 'string'
            },
            'commands': {
                'turn_on': {'method': 'POST', 'topic': 'devices/lights/on'},
                'turn_off': {'method': 'POST', 'topic': 'devices/lights/off'},
                'set_brightness': {'method': 'POST', 'topic': 'devices/lights/brightness'},
                'set_color': {'method': 'POST', 'topic': 'devices/lights/color'}
            }
        }
    )

    # Home automation hub endpoint
    cli.create_endpoint(
        uri='mqtt://localhost:1883/home/status',
        data={
            'topic': 'home/status',
            'qos': 2,
            'retain': True,
            'device': {
                'id': 'home_hub_01',
                'type': 'hub',
                'location': 'office',
                'connected_devices': [
                    'temp_sensor_01',
                    'motion_sensor_01',
                    'smart_light_01'
                ]
            },
            'schema': {
                'devices_online': 'int',
                'last_update': 'string',
                'system_status': 'string',
                'alerts': 'array'
            }
        }
    )

    print("\nMQTT IoT endpoints created:")
    print("\n1. Temperature Sensor:")
    print("   - Topic: sensors/temperature")
    print("   - QoS: 1")
    print("   - Location: Living Room")
    print("   - Update Interval: 60s")
    
    print("\n2. Motion Sensor:")
    print("   - Topic: sensors/motion")
    print("   - QoS: 2")
    print("   - Location: Entrance")
    print("   - Sensitivity: High")
    
    print("\n3. Smart Light:")
    print("   - Topic: devices/lights")
    print("   - QoS: 1")
    print("   - Location: Living Room")
    print("   - Capabilities: Dimming, Color")
    
    print("\n4. Home Hub:")
    print("   - Topic: home/status")
    print("   - QoS: 2")
    print("   - Location: Office")
    print("   - Connected Devices: 3")

def simulate_iot_communication():
    """
    Example of how to simulate IoT device communication
    """
    cli = UriPointCLI()

    # Simulate temperature sensor reading
    temp_data = {
        'temperature': 22.5,
        'humidity': 45.0,
        'battery': 85,
        'timestamp': '2024-11-12T00:15:00Z'
    }
    cli.publish('mqtt://localhost:1883/sensors/temperature', temp_data)

    # Simulate motion detection
    motion_data = {
        'motion_detected': True,
        'light_level': 120,
        'battery': 90,
        'timestamp': '2024-11-12T00:15:01Z'
    }
    cli.publish('mqtt://localhost:1883/sensors/motion', motion_data)

    # Control smart light
    light_command = {
        'state': True,
        'brightness': 75,
        'color': '#FF9900',
        'timestamp': '2024-11-12T00:15:02Z'
    }
    cli.publish('mqtt://localhost:1883/devices/lights', light_command)

    # Update hub status
    hub_status = {
        'devices_online': 3,
        'last_update': '2024-11-12T00:15:03Z',
        'system_status': 'healthy',
        'alerts': []
    }
    cli.publish('mqtt://localhost:1883/home/status', hub_status)

if __name__ == '__main__':
    print("Setting up MQTT IoT endpoints...")
    setup_mqtt_endpoints()
    
    print("\nSimulating IoT device communication...")
    simulate_iot_communication()
