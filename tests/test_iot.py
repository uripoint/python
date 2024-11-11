"""
Tests for IoT protocol handlers
"""
import pytest
from uripoint.protocols import (
    MQTTHandler,
    get_protocol_handler
)

def test_mqtt_handler():
    """Test MQTT protocol handler"""
    handler = MQTTHandler()
    
    # Test valid temperature sensor configuration
    temp_sensor_config = {
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
            'battery': 'int'
        }
    }
    assert handler.validate_config(temp_sensor_config) is True
    
    # Test valid motion sensor configuration
    motion_sensor_config = {
        'topic': 'sensors/motion',
        'qos': 2,
        'retain': False,
        'device': {
            'id': 'motion_sensor_01',
            'type': 'motion',
            'location': 'entrance'
        }
    }
    assert handler.validate_config(motion_sensor_config) is True
    
    # Test invalid QoS level
    invalid_qos_config = {
        'topic': 'sensors/test',
        'qos': 3,  # Invalid QoS level (should be 0, 1, or 2)
        'retain': True
    }
    with pytest.raises(ValueError, match="Invalid QoS level: 3"):
        handler.validate_config(invalid_qos_config)

def test_mqtt_device_types():
    """Test MQTT handler with different device types"""
    handler = MQTTHandler()
    
    # Test temperature sensor
    temp_sensor = {
        'topic': 'sensors/temperature',
        'qos': 1,
        'device': {
            'type': 'temperature',
            'schema': {
                'temperature': 'float',
                'humidity': 'float'
            }
        }
    }
    assert handler.validate_config(temp_sensor) is True
    
    # Test smart light
    smart_light = {
        'topic': 'devices/lights',
        'qos': 1,
        'device': {
            'type': 'light',
            'capabilities': ['dimming', 'color']
        }
    }
    assert handler.validate_config(smart_light) is True
    
    # Test home hub
    home_hub = {
        'topic': 'home/status',
        'qos': 2,
        'device': {
            'type': 'hub',
            'connected_devices': ['temp_sensor_01', 'light_01']
        }
    }
    assert handler.validate_config(home_hub) is True

def test_mqtt_message_handling():
    """Test MQTT message handling"""
    handler = MQTTHandler()
    
    # Test temperature sensor data
    temp_data = {
        'config': {
            'topic': 'sensors/temperature',
            'qos': 1,
            'response': {
                'temperature': 22.5,
                'humidity': 45.0,
                'battery': 85
            }
        }
    }
    response = handler.handle_request(temp_data)
    assert 'topic' in response
    assert 'qos' in response
    assert 'status' in response
    
    # Test motion sensor data
    motion_data = {
        'config': {
            'topic': 'sensors/motion',
            'qos': 2,
            'response': {
                'motion_detected': True,
                'light_level': 120
            }
        }
    }
    response = handler.handle_request(motion_data)
    assert 'topic' in response
    assert 'qos' in response
    assert 'status' in response

def test_mqtt_error_handling():
    """Test MQTT error handling"""
    handler = MQTTHandler()
    
    # Test with invalid endpoint info
    with pytest.raises(KeyError):
        handler.handle_request({})
    
    # Test with invalid QoS
    with pytest.raises(ValueError, match="Invalid QoS level"):
        handler.handle_request({
            'config': {
                'topic': 'test',
                'qos': 5  # Invalid QoS
            }
        })

def test_mqtt_connection():
    """Test MQTT connection handling"""
    handler = MQTTHandler()
    
    # Test basic connection
    assert handler.connect() is True
    
    # Test protocol factory
    mqtt_handler = get_protocol_handler('mqtt')
    assert isinstance(mqtt_handler, MQTTHandler)
    assert mqtt_handler.connect() is True

def test_mqtt_device_commands():
    """Test MQTT device command handling"""
    handler = MQTTHandler()
    
    # Test smart light commands
    light_config = {
        'topic': 'devices/lights',
        'qos': 1,
        'device': {
            'type': 'light',
            'capabilities': ['dimming', 'color']
        },
        'commands': {
            'turn_on': {'method': 'POST', 'topic': 'devices/lights/on'},
            'set_brightness': {'method': 'POST', 'topic': 'devices/lights/brightness'}
        }
    }
    assert handler.validate_config(light_config) is True
    
    # Test thermostat commands
    thermostat_config = {
        'topic': 'devices/thermostat',
        'qos': 1,
        'device': {
            'type': 'thermostat',
            'capabilities': ['heating', 'cooling']
        },
        'commands': {
            'set_temperature': {'method': 'POST', 'topic': 'devices/thermostat/temp'},
            'set_mode': {'method': 'POST', 'topic': 'devices/thermostat/mode'}
        }
    }
    assert handler.validate_config(thermostat_config) is True

def test_mqtt_device_status():
    """Test MQTT device status handling"""
    handler = MQTTHandler()
    
    # Test online status
    status_data = {
        'config': {
            'topic': 'devices/status',
            'qos': 1,
            'response': {
                'device_id': 'temp_sensor_01',
                'status': 'online',
                'last_seen': '2024-11-12T00:15:00Z',
                'battery': 85
            }
        }
    }
    response = handler.handle_request(status_data)
    assert 'status' in response
    
    # Test offline detection
    offline_data = {
        'config': {
            'topic': 'devices/status',
            'qos': 1,
            'response': {
                'device_id': 'temp_sensor_01',
                'status': 'offline',
                'last_seen': '2024-11-12T00:10:00Z'
            }
        }
    }
    response = handler.handle_request(offline_data)
    assert 'status' in response
