"""
Example demonstrating CoAP protocol support in UriPoint for IoT devices
"""
from uripoint import UriPointCLI

def setup_coap_endpoints():
    """Setup CoAP endpoints for IoT devices"""
    cli = UriPointCLI()

    # Temperature sensor endpoint
    cli.create_endpoint(
        uri='coap://localhost:5683/sensors/temperature',
        data={
            'resource_type': 'temperature',
            'interface': 'sensor',
            'content_format': 'application/json',
            'observable': True,
            'max_age': 60,
            'response': {
                'temperature': 22.5,
                'unit': 'celsius',
                'timestamp': '2024-01-01T00:00:00Z'
            },
            'options': {
                'block_size': 64,
                'observe': True
            }
        }
    )

    # Light control endpoint
    cli.create_endpoint(
        uri='coap://localhost:5683/actuators/light',
        data={
            'resource_type': 'light',
            'interface': 'actuator',
            'content_format': 'application/json',
            'methods': ['GET', 'PUT', 'POST'],
            'response': {
                'state': 'off',
                'brightness': 0,
                'color': '#FFFFFF'
            }
        }
    )

    # Device configuration endpoint
    cli.create_endpoint(
        uri='coap://localhost:5683/.well-known/core',
        data={
            'resource_type': 'core.rd',
            'content_format': 'application/link-format',
            'response': {
                'links': [
                    '</sensors/temperature>;rt=temperature;if=sensor',
                    '</actuators/light>;rt=light;if=actuator',
                    '</system/info>;rt=system'
                ]
            }
        }
    )

    # System information endpoint
    cli.create_endpoint(
        uri='coap://localhost:5683/system/info',
        data={
            'resource_type': 'system',
            'interface': 'system',
            'content_format': 'application/json',
            'response': {
                'device_id': 'iot-device-001',
                'firmware_version': '1.0.0',
                'battery_level': 85,
                'uptime': 3600
            }
        }
    )

    # Batch update endpoint
    cli.create_endpoint(
        uri='coap://localhost:5683/batch',
        data={
            'resource_type': 'batch',
            'interface': 'batch',
            'content_format': 'application/json',
            'methods': ['POST'],
            'response': {
                'status': 'success',
                'processed': 0
            }
        }
    )

    print("\nCoAP endpoints created:")
    print("1. Temperature Sensor:")
    print("   - URI: coap://localhost:5683/sensors/temperature")
    print("   - Type: Observable Sensor")
    print("   - Format: JSON")
    
    print("\n2. Light Control:")
    print("   - URI: coap://localhost:5683/actuators/light")
    print("   - Type: Actuator")
    print("   - Methods: GET, PUT, POST")
    
    print("\n3. Core Discovery:")
    print("   - URI: coap://localhost:5683/.well-known/core")
    print("   - Type: Resource Directory")
    
    print("\n4. System Info:")
    print("   - URI: coap://localhost:5683/system/info")
    print("   - Type: System Interface")

def test_coap_endpoints():
    """Test CoAP endpoints"""
    cli = UriPointCLI()

    # Test temperature sensor
    print("\nTesting temperature sensor...")
    cli.subscribe(
        'coap://localhost:5683/sensors/temperature',
        lambda data: print(f"Temperature update: {data}")
    )

    # Test light control
    print("\nTesting light control...")
    light_command = {
        'state': 'on',
        'brightness': 75,
        'color': '#FF9900'
    }
    cli.publish('coap://localhost:5683/actuators/light', light_command)

    # Test resource discovery
    print("\nTesting resource discovery...")
    cli.get('coap://localhost:5683/.well-known/core')

    # Test batch update
    print("\nTesting batch update...")
    batch_data = {
        'updates': [
            {
                'uri': '/sensors/temperature',
                'value': {'temperature': 23.5}
            },
            {
                'uri': '/actuators/light',
                'value': {'state': 'off'}
            }
        ]
    }
    cli.publish('coap://localhost:5683/batch', batch_data)

def setup_coap_options():
    """Configure CoAP protocol options"""
    return {
        'multicast': True,
        'retransmission': {
            'timeout': 2,
            'max_retransmit': 4
        },
        'block_transfer': {
            'block_size': 64,
            'block2': True
        },
        'observe': {
            'max_age': 60,
            'notify_interval': 5
        },
        'security': {
            'dtls': True,
            'psk': {
                'identity': 'client1',
                'key': 'secret-key'
            }
        }
    }

if __name__ == '__main__':
    print("Setting up CoAP endpoints...")
    setup_coap_endpoints()
    
    print("\nTesting CoAP endpoints...")
    test_coap_endpoints()
