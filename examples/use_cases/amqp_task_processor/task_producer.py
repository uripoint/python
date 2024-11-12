"""
AMQP Task Producer using UriPoint
Generates and submits various types of tasks to the processing system
"""

from uripoint import UriPointCLI
import json
import time
import random
from datetime import datetime
import uuid

class TaskProducer:
    def __init__(self):
        self.cli = UriPointCLI()
        self.setup_endpoints()

    def setup_endpoints(self):
        # Setup task queue endpoints with different priorities
        task_types = ['image_processing', 'data_analysis', 'report_generation']
        priorities = ['high', 'medium', 'low']

        for task_type in task_types:
            for priority in priorities:
                self.cli.create_endpoint(
                    uri=f'amqp://rabbitmq:5672/tasks/{task_type}/{priority}',
                    data={
                        'exchange': 'tasks',
                        'exchange_type': 'topic',
                        'routing_key': f'{task_type}.{priority}',
                        'queue': f'{task_type}_{priority}',
                        'durable': True
                    }
                )

        # Setup dead letter queue
        self.cli.create_endpoint(
            uri='amqp://rabbitmq:5672/dead_letter',
            data={
                'exchange': 'dead_letter',
                'exchange_type': 'fanout',
                'queue': 'failed_tasks',
                'durable': True
            }
        )

    def generate_image_task(self, priority):
        operations = ['resize', 'convert', 'filter']
        formats = ['jpg', 'png', 'webp']
        
        return {
            'task_id': str(uuid.uuid4()),
            'type': 'image_processing',
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'data': {
                'operation': random.choice(operations),
                'input_format': random.choice(formats),
                'output_format': random.choice(formats),
                'dimensions': {
                    'width': random.randint(100, 1000),
                    'height': random.randint(100, 1000)
                },
                'quality': random.randint(70, 100)
            }
        }

    def generate_analysis_task(self, priority):
        analysis_types = ['aggregation', 'statistics', 'pattern_detection']
        data_sources = ['sales', 'user_behavior', 'system_metrics']
        
        return {
            'task_id': str(uuid.uuid4()),
            'type': 'data_analysis',
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'data': {
                'analysis_type': random.choice(analysis_types),
                'data_source': random.choice(data_sources),
                'time_range': {
                    'start': (datetime.now().timestamp() - 86400),  # 24 hours ago
                    'end': datetime.now().timestamp()
                },
                'parameters': {
                    'sample_size': random.randint(1000, 10000),
                    'confidence_level': random.uniform(0.90, 0.99)
                }
            }
        }

    def generate_report_task(self, priority):
        report_types = ['daily_summary', 'performance_metrics', 'audit_report']
        formats = ['pdf', 'html', 'excel']
        
        return {
            'task_id': str(uuid.uuid4()),
            'type': 'report_generation',
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'data': {
                'report_type': random.choice(report_types),
                'format': random.choice(formats),
                'recipients': [f'user{i}@example.com' for i in range(random.randint(1, 3))],
                'include_charts': random.choice([True, False]),
                'template_id': f'template_{random.randint(1, 5)}'
            }
        }

    def submit_task(self, task):
        task_type = task['type']
        priority = task['priority']
        
        print(f"Submitting {priority} priority {task_type} task: {task['task_id']}")
        
        self.cli.publish(
            f'amqp://rabbitmq:5672/tasks/{task_type}/{priority}',
            task
        )

    def simulate_task_generation(self):
        print("Starting task generation simulation...")
        
        task_generators = {
            'image_processing': self.generate_image_task,
            'data_analysis': self.generate_analysis_task,
            'report_generation': self.generate_report_task
        }

        priorities = ['high', 'medium', 'low']
        priority_weights = [0.2, 0.5, 0.3]  # 20% high, 50% medium, 30% low priority

        while True:
            try:
                # Randomly select task type and priority
                task_type = random.choice(list(task_generators.keys()))
                priority = random.choices(priorities, priority_weights)[0]

                # Generate and submit task
                task = task_generators[task_type](priority)
                self.submit_task(task)

                # Random delay between tasks
                time.sleep(random.uniform(1, 5))

            except Exception as e:
                print(f"Error generating task: {e}")
                time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    producer = TaskProducer()
    producer.simulate_task_generation()
