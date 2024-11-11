"""
MQTT Protocol Example for UriPoint
Demonstrates IoT device communication using MQTT protocol
"""

from uripoint import UriPointCLI

def setup_mqtt_endpoint():
    # Create CLI instance
    cli = UriPointCLI()

    # Create MQTT endpoint for temperature sensor
    cli.create_endpoint(
        uri='mqtt://localhost:1883/sensors/temperature',
        data={
            'topic': 'sensors/temperature',
            'qos': 1,
            'retain': True
        }
    )

    # Create MQTT endpoint for humidity sensor
    cli.create_endpoint(
        uri='mqtt://localhost:1883/sensors/humidity',
        data={
            'topic': 'sensors/humidity',
            'qos': 1,
            'retain': True
        }
    )

def simulate_sensor_data():
    import random
    import time
    
    cli = UriPointCLI()
    
    while True:
        # Simulate temperature reading
        temperature = 20 + random.uniform(-5, 5)
        cli.publish(
            'mqtt://localhost:1883/sensors/temperature',
            {'temperature': temperature}
        )
        
        # Simulate humidity reading
        humidity = 50 + random.uniform(-10, 10)
        cli.publish(
            'mqtt://localhost:1883/sensors/humidity',
            {'humidity': humidity}
        )
        
        time.sleep(5)

if __name__ == '__main__':
    setup_mqtt_endpoint()
    simulate_sensor_data()
