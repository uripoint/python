# AMQP Distributed Task Processing System

## Why is this interesting?

AMQP (Advanced Message Queuing Protocol) is particularly interesting for distributed task processing because:

1. **Message Reliability**: Guarantees message delivery with acknowledgments and persistence
2. **Work Queue Pattern**: Enables fair distribution of time-consuming tasks across multiple workers
3. **Message Routing**: Supports complex routing patterns with exchanges and bindings
4. **Load Balancing**: Automatically distributes tasks among available workers
5. **Dead Letter Handling**: Provides mechanisms for handling failed tasks

## Use Case Description

This example implements a distributed task processing system that demonstrates:
- Multiple task types (image processing, data analysis, report generation)
- Priority queues for urgent tasks
- Dead letter queues for failed tasks
- Task result handling
- Worker scaling

## Components

1. `task_producer.py` - Generates and submits tasks to the system
2. `task_worker.py` - Processes tasks from queues
3. `result_collector.py` - Collects and processes task results
4. `Dockerfile` - Container configuration for each component
5. `docker-compose.yml` - Multi-container setup with RabbitMQ and application components

## Running the Example

1. Start the containers:
```bash
docker-compose up -d
```

2. Scale workers:
```bash
docker-compose up -d --scale worker=3
```

3. Monitor the output:
```bash
docker-compose logs -f
```

4. Stop the system:
```bash
docker-compose down
```

## URI Endpoints

- `amqp://rabbitmq:5672/tasks/image_processing` - Image processing tasks
- `amqp://rabbitmq:5672/tasks/data_analysis` - Data analysis tasks
- `amqp://rabbitmq:5672/tasks/report_generation` - Report generation tasks
- `amqp://rabbitmq:5672/results` - Task results
- `amqp://rabbitmq:5672/dead_letter` - Failed tasks

## Task Types

1. Image Processing Tasks:
   - Image resizing
   - Format conversion
   - Filter application

2. Data Analysis Tasks:
   - Data aggregation
   - Statistical analysis
   - Pattern detection

3. Report Generation Tasks:
   - PDF report creation
   - Data visualization
   - Email report distribution
