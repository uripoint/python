"""
AMQP Result Collector using UriPoint
Collects and processes task results and handles failed tasks
"""

from uripoint import UriPointCLI
import json
import time
from datetime import datetime
import uuid
from collections import defaultdict
import statistics

class ResultCollector:
    def __init__(self):
        self.cli = UriPointCLI()
        self.collector_id = str(uuid.uuid4())[:8]
        self.setup_endpoints()
        self.stats = defaultdict(list)
        self.last_report_time = datetime.now()
        self.report_interval = 60  # Generate report every 60 seconds

    def setup_endpoints(self):
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

    def process_result(self, result):
        """Process a completed task result"""
        task_id = result['task_id']
        worker_id = result['worker_id']
        processing_time = result['processing_time']

        print(f"Received result for task {task_id} from worker {worker_id}")
        print(f"Processing time: {processing_time:.2f} seconds")

        # Store statistics
        task_type = self.determine_task_type(result)
        self.stats[task_type].append(processing_time)

    def process_failure(self, failure):
        """Process a failed task"""
        task_id = failure['task_id']
        worker_id = failure['worker_id']
        error = failure['error']

        print(f"Processing failure for task {task_id} from worker {worker_id}")
        print(f"Error: {error}")
        print("Traceback:")
        print(failure['traceback'])

        # Here you could implement retry logic or alert notifications
        # For now, we'll just log the failure
        print(f"Task {task_id} permanently failed")

    def determine_task_type(self, result):
        """Determine task type from result data"""
        if 'output_url' in result and 'output_url' in result:
            return 'image_processing'
        elif 'results' in result and 'correlation_coefficient' in result['results']:
            return 'data_analysis'
        elif 'report_url' in result and 'page_count' in result:
            return 'report_generation'
        return 'unknown'

    def generate_statistics_report(self):
        """Generate a report of processing statistics"""
        now = datetime.now()
        print("\n=== Processing Statistics Report ===")
        print(f"Time: {now.isoformat()}")
        print("-----------------------------------")

        for task_type, times in self.stats.items():
            if times:
                avg_time = statistics.mean(times)
                min_time = min(times)
                max_time = max(times)
                if len(times) > 1:
                    stddev = statistics.stdev(times)
                else:
                    stddev = 0

                print(f"\nTask Type: {task_type}")
                print(f"Total processed: {len(times)}")
                print(f"Average time: {avg_time:.2f}s")
                print(f"Min time: {min_time:.2f}s")
                print(f"Max time: {max_time:.2f}s")
                print(f"Standard deviation: {stddev:.2f}s")

        print("\n===================================")
        
        # Clear statistics after reporting
        self.stats.clear()
        self.last_report_time = now

    def should_generate_report(self):
        """Check if it's time to generate a new report"""
        time_since_last = (datetime.now() - self.last_report_time).total_seconds()
        return time_since_last >= self.report_interval

    def start_collecting(self):
        """Start collecting and processing results"""
        print(f"Result Collector {self.collector_id} starting up...")

        while True:
            try:
                # Check for completed tasks
                result = self.cli.get('amqp://rabbitmq:5672/results')
                if result:
                    self.process_result(result)

                # Check for failed tasks
                failure = self.cli.get('amqp://rabbitmq:5672/dead_letter')
                if failure:
                    self.process_failure(failure)

                # Generate periodic statistics report
                if self.should_generate_report():
                    self.generate_statistics_report()

                # Small delay to prevent busy-waiting
                time.sleep(0.1)

            except Exception as e:
                print(f"Error in result collection loop: {e}")
                time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    collector = ResultCollector()
    collector.start_collecting()
