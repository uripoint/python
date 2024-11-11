"""
AMQP Protocol Example for UriPoint
Demonstrates message queuing using RabbitMQ
"""

from uripoint import UriPointCLI

def setup_amqp_endpoints():
    # Create CLI instance
    cli = UriPointCLI()

    # Create AMQP endpoint for order processing
    cli.create_endpoint(
        uri='amqp://localhost:5672/orders',
        data={
            'exchange': 'order_exchange',
            'exchange_type': 'direct',
            'queue': 'order_queue',
            'routing_key': 'new_order',
            'durable': True
        }
    )

    # Create AMQP endpoint for logging
    cli.create_endpoint(
        uri='amqp://localhost:5672/logs',
        data={
            'exchange': 'log_exchange',
            'exchange_type': 'topic',
            'queue': 'log_queue',
            'routing_key': 'system.*',
            'durable': True
        }
    )

def process_orders():
    cli = UriPointCLI()
    
    # Publish new order
    order_data = {
        'order_id': '12345',
        'customer': 'John Doe',
        'items': [
            {'product': 'Widget A', 'quantity': 2},
            {'product': 'Widget B', 'quantity': 1}
        ],
        'total': 59.97
    }
    
    cli.publish(
        'amqp://localhost:5672/orders',
        order_data
    )
    
    # Subscribe to order processing results
    def order_callback(message):
        print(f"Order processed: {message}")
    
    cli.subscribe(
        'amqp://localhost:5672/orders/results',
        order_callback
    )

def handle_logging():
    cli = UriPointCLI()
    
    # Publish system logs
    log_data = {
        'timestamp': '2023-07-20T11:00:00',
        'level': 'INFO',
        'service': 'order_processor',
        'message': 'Successfully processed order #12345'
    }
    
    cli.publish(
        'amqp://localhost:5672/logs',
        log_data,
        routing_key='system.info'
    )
    
    # Subscribe to error logs
    def error_log_callback(message):
        print(f"Error log received: {message}")
    
    cli.subscribe(
        'amqp://localhost:5672/logs',
        error_log_callback,
        routing_key='system.error'
    )

if __name__ == '__main__':
    setup_amqp_endpoints()
    process_orders()
    handle_logging()
