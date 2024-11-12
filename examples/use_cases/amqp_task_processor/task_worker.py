"""
AMQP Task Worker using UriPoint
Processes tasks from queues and handles different task types
"""

from uripoint import UriPointCLI
import json
import time
import random
from datetime import datetime
import uuid
import traceback

class TaskWorker:
    def __init__(self):
        self.cli = UriPointCLI()
        self.worker_id = str(uuid.uuid4())[:8]
        self.setup_endpoints()

    def setup_endpoints(self):
        # Setup task queue endpoints for consumption
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
                        'durable': True,
                        'prefetch_count': 1  # Process one message at a time
                    }
                )

        # Setup results queue
        self.cli.create_endpoint(
            uri='amqp://rabbitmq:5672/results',
            data={
                'exchange': 'results',
                'exchange_type': 'direct',
                'queue': 'task_results',
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

    def process_image(self, task_data):
        """Simulate image processing operations"""
        operation = task_data['operation']
        print(f"Processing image: {operation}")
        
        # Simulate processing time based on operation
        if operation == 'resize':
            time.sleep(random.uniform(0.5, 2))
        elif operation == 'convert':
            time.sleep(random.uniform(0.3, 1))
        elif operation == 'filter':
            time.sleep(random.uniform(1, 3))

        return {
            'output_url': f'https://example.com/processed/{uuid.uuid4()}.{task_data["output_format"]}',
            'processing_time': random.uniform(0.5, 3)
        }

    def process_analysis(self, task_data):
        """Simulate data analysis operations"""
        analysis_type = task_data['analysis_type']
        print(f"Performing analysis: {analysis_type}")
        
        # Simulate analysis time
        time.sleep(random.uniform(2, 5))

        return {
            'results': {
                'sample_size': task_data['parameters']['sample_size'],
                'confidence_interval': random.uniform(0.1, 0.5),
                'p_value': random.uniform(0, 0.05),
                'correlation_coefficient': random.uniform(-1, 1)
            },
            'processing_time': random.uniform(2, 5)
        }

    def process_report(self, task_data):
        """Simulate report generation operations"""
        report_type = task_data['report_type']
        print(f"Generating report: {report_type}")
        
        # Simulate report generation time
        time.sleep(random.uniform(1, 4))

        return {
            'report_url': f'https://example.com/reports/{uuid.uuid4()}.{task_data["format"]}',
            'page_count': random.randint(5, 50),
            'processing_time': random.uniform(1, 4)
        }

    def process_task(self, task):
        """Process a task based on its type"""
        task_type = task['type']
        task_data = task['data']
        
        processors = {
            'image_processing': self.process_image,
            'data_analysis': self.process_analysis,
            'report_generation': self.process_report
        }

        try:
            print(f"Worker {self.worker_id} processing {task_type} task: {task['task_id']}")
            
            # Process the task
            result = processors[task_type](task_data)
            
            # Add metadata to result
            result.update({
                'task_id': task['task_id'],
                'worker_id': self.worker_id,
                'completed_at': datetime.now().isoformat(),
                'status': 'completed'
            })

            # Publish result
            self.cli.publish(
                'amqp://rabbitmq:5672/results',
                result
            )
            print(f"Task {task['task_id']} completed successfully")

        except Exception as e:
            error_data = {
                'task_id': task['task_id'],
                'worker_id': self.worker_id,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'failed_at': datetime.now().isoformat(),
                'task_data': task
            }
            
            # Send to dead letter queue
            self.cli.publish(
                'amqp://rabbitmq:5672/dead_letter',
                error_data
            )
            print(f"Task {task['task_id']} failed: {str(e)}")

    def start_processing(self):
        """Start processing tasks from all queues"""
        print(f"Worker {self.worker_id} starting up...")
        
        task_types = ['image_processing', 'data_analysis', 'report_generation']
        priorities = ['high', 'medium', 'low']

        while True:
            try:
                # Process high priority tasks first
                for priority in priorities:
                    for task_type in task_types:
                        queue_uri = f'amqp://rabbitmq:5672/tasks/{task_type}/{priority}'
                        
                        # Try to get a task from the queue
                        task = self.cli.get(queue_uri)
                        if task:
                            self.process_task(task)
                
                # Small delay to prevent busy-waiting
                time.sleep(0.1)

            except Exception as e:
                print(f"Error in task processing loop: {e}")
                time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    worker = TaskWorker()
    worker.start_processing()
