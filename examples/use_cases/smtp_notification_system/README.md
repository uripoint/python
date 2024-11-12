# SMTP Email Notification System

## Why is this interesting?

SMTP is particularly interesting for automated email communications because:

1. **Universal Compatibility**: SMTP is the standard protocol for email delivery across all platforms
2. **Rich Content Support**: Enables sending HTML emails with formatting, images, and attachments
3. **Delivery Reliability**: Built-in retry mechanisms and delivery status notifications
4. **Template Support**: Can be combined with templating engines for dynamic content
5. **Scheduling Capabilities**: Perfect for timing-sensitive communications

## Use Case Description

This example implements an email notification system that demonstrates:
- Email template rendering with dynamic content
- Scheduled notifications (daily digests, weekly reports)
- Event-triggered emails (user actions, system alerts)
- HTML and plain text email support
- Email queue management

## Components

1. `app.py` - Main application implementing the notification system
2. `Dockerfile` - Container configuration for the application
3. `docker-compose.yml` - Multi-container setup with SMTP server and application
4. `templates/` - Directory containing email templates
   - welcome.html
   - alert.html
   - digest.html

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

- `smtp://mailhog:1025/welcome` - New user welcome emails
- `smtp://mailhog:1025/alert` - System alert notifications
- `smtp://mailhog:1025/digest` - Daily activity digest emails
- `smtp://mailhog:1025/report` - Weekly performance reports

## Email Templates

The system includes several email templates:
- Welcome Email: Sent to new users with getting started information
- Alert Notification: Used for system alerts and important updates
- Daily Digest: Summary of daily activities and updates
- Weekly Report: Comprehensive weekly performance metrics
