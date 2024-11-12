# Redis Session Manager and Notification System

## Why is this interesting?

Redis is particularly interesting for session management and real-time notifications because:

1. **In-Memory Performance**: Redis's in-memory nature provides ultra-fast access to session data
2. **Data Structures**: Rich data structures (Strings, Lists, Sets, Hashes) enable complex session data storage
3. **Pub/Sub Capabilities**: Built-in publish/subscribe for real-time notifications
4. **Key Expiration**: Automatic session expiration handling with TTL feature
5. **Atomic Operations**: Ensures data consistency in high-concurrency scenarios

## Use Case Description

This example implements a session management and notification system that demonstrates:
- User session handling with automatic expiration
- Real-time notifications using Redis Pub/Sub
- Rate limiting for API access
- User presence tracking
- Activity logging

## Components

1. `app.py` - Main application implementing session management and notifications
2. `Dockerfile` - Container configuration for the application
3. `docker-compose.yml` - Multi-container setup with Redis and application

## Running the Example

1. Start the containers:
```bash
docker-compose up -d
```

2. Monitor the output:
```bash
docker-compose logs -f app
```

3. Stop the system:
```bash
docker-compose down
```

## URI Endpoints

- `redis://redis:6379/sessions/{user_id}` - User session data
- `redis://redis:6379/notifications/{user_id}` - User notifications
- `redis://redis:6379/presence/{user_id}` - User presence information
- `redis://redis:6379/ratelimit/{api_key}` - API rate limiting
