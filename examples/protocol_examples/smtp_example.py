"""
SMTP Protocol Example for UriPoint
Demonstrates email handling capabilities
"""

from uripoint import UriPointCLI

def setup_smtp_endpoints():
    # Create CLI instance
    cli = UriPointCLI()

    # Create SMTP endpoint for sending notifications
    cli.create_endpoint(
        uri='smtp://smtp.gmail.com:587/notifications',
        data={
            'username': 'notifications@example.com',
            'password': 'app_specific_password',
            'use_tls': True,
            'timeout': 30
        }
    )

    # Create SMTP endpoint for system alerts
    cli.create_endpoint(
        uri='smtp://smtp.gmail.com:587/alerts',
        data={
            'username': 'alerts@example.com',
            'password': 'app_specific_password',
            'use_tls': True,
            'timeout': 15
        }
    )

def send_example_emails():
    cli = UriPointCLI()
    
    # Send a notification email
    notification_data = {
        'to': 'user@example.com',
        'subject': 'New Account Activity',
        'body': 'Your account was accessed from a new device.',
        'html': True,
        'attachments': []
    }
    cli.send('smtp://smtp.gmail.com:587/notifications', notification_data)
    
    # Send a system alert
    alert_data = {
        'to': ['admin@example.com', 'ops@example.com'],
        'subject': 'CRITICAL: System CPU Usage High',
        'body': 'System CPU usage has exceeded 90% for 5 minutes.',
        'priority': 'high',
        'html': False
    }
    cli.send('smtp://smtp.gmail.com:587/alerts', alert_data)

def setup_email_templates():
    # Register email templates
    cli = UriPointCLI()
    
    welcome_template = {
        'subject': 'Welcome to Our Service',
        'body': '''
        Dear {name},
        
        Welcome to our service! We're excited to have you on board.
        
        Best regards,
        The Team
        ''',
        'html': True
    }
    
    cli.register_template('smtp://smtp.gmail.com:587/notifications/welcome', welcome_template)

if __name__ == '__main__':
    setup_smtp_endpoints()
    setup_email_templates()
    send_example_emails()
