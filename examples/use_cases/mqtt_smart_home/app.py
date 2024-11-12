"""
Smart Home Monitoring System using MQTT and UriPoint
"""

from uripoint import UriPointCLI
import random
import time
import json
from datetime import datetime

class SmartHome:
    def __init__(self):
        self.cli = UriPointCLI()
        self.rooms = ['living_room', 'bedroom', 'kitchen', 'bathroom']
        self.motion_locations = ['entrance', 'hallway', 'garage', 'backyard']
        self.setup_endpoints()

    def setup_endpoints(self):
        # Temperature endpoints for each room
        for room in self.rooms:
            self.cli.create_endpoint(
                uri=f'mqtt://broker:1883/home/temperature/{room}',
                data={
                    'topic': f'home/temperature/{room}',
                    'qos': 1,
                    'retain': True
                }
            )

        # Motion detection endpoints
        for location in self.motion_locations:
            self.cli.create_endpoint(
                uri=f'mqtt://broker:1883/home/motion/{location}',
                data={
                    'topic': f'home/motion/{location}',
                    'qos': 1,
                    'retain': False
                }
            )

        # Light control endpoints
        for room in self.rooms:
            self.cli.create_endpoint(
                uri=f'mqtt://broker:1883/home/lights/{room}',
                data={
                    'topic': f'home/lights/{room}',
                    'qos': 1,
                    'retain': True
                }
            )

        # Energy monitoring endpoint
        self.cli.create_endpoint(
            uri='mqtt://broker:1883/home/energy',
            data={
                'topic': 'home/energy',
                'qos': 1,
                'retain': True
            }
        )

    def simulate_temperature(self):
        for room in self.rooms:
            # Simulate different base temperatures for different rooms
            base_temp = {
                'living_room': 22,
                'bedroom': 20,
                'kitchen': 23,
                'bathroom': 21
            }
            temperature = base_temp[room] + random.uniform(-1, 1)
            
            self.cli.publish(
                f'mqtt://broker:1883/home/temperature/{room}',
                {
                    'temperature': round(temperature, 2),
                    'unit': 'celsius',
                    'timestamp': datetime.now().isoformat()
                }
            )

    def simulate_motion(self):
        # Randomly trigger motion events
        if random.random() < 0.3:  # 30% chance of motion detection
            location = random.choice(self.motion_locations)
            self.cli.publish(
                f'mqtt://broker:1883/home/motion/{location}',
                {
                    'motion_detected': True,
                    'timestamp': datetime.now().isoformat()
                }
            )

    def simulate_lights(self):
        # Simulate light states based on time of day
        hour = datetime.now().hour
        for room in self.rooms:
            # Lights are more likely to be on in evening/night
            light_on = random.random() < 0.8 if (hour < 6 or hour > 18) else random.random() < 0.2
            self.cli.publish(
                f'mqtt://broker:1883/home/lights/{room}',
                {
                    'state': 'on' if light_on else 'off',
                    'brightness': random.randint(50, 100) if light_on else 0,
                    'timestamp': datetime.now().isoformat()
                }
            )

    def simulate_energy(self):
        # Simulate total home energy consumption
        base_consumption = 1000  # base watts
        variation = random.uniform(-100, 100)
        
        self.cli.publish(
            'mqtt://broker:1883/home/energy',
            {
                'total_watts': round(base_consumption + variation, 2),
                'timestamp': datetime.now().isoformat()
            }
        )

    def run(self):
        print("Starting Smart Home simulation...")
        while True:
            try:
                self.simulate_temperature()
                self.simulate_motion()
                self.simulate_lights()
                self.simulate_energy()
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                print(f"Error in simulation: {e}")
                time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    smart_home = SmartHome()
    smart_home.run()
