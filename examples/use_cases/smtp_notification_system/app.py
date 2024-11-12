"""
SMTP Email Notification System using UriPoint
"""

from uripoint import UriPointCLI
import json
import time
from datetime import datetime, timedelta
import random
from pathlib import Path
import jinja2
import psutil

class EmailNotificationSystem:
    def __init__(self):
        self.cli = UriPointCLI()
        self.template_dir = Path('templates')
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir)
        )
        self.setup_endpoints()

    def setup_endpoints(self):
        # Setup endpoints for different email types
        endpoints = ['welcome', 'alert', 'digest', 'report']
        for endpoint in endpoints:
            self.cli.create_endpoint(
                uri=f'smtp://mailhog:1025/{endpoint}',
                data={
                    'from_address': 'notifications@example.com',
                    'subject_prefix': f'[{endpoint.upper()}] '
                }
            )

    def send_welcome_email(self, user_data):
        template = self.jinja_env.get_template('welcome.html')
        html_content = template.render(
            name=user_data['name'],
            username=user_data['username'],
            email=user_data['email'],
            join_date=datetime.now().strftime('%Y-%m-%d'),
            dashboard_url='https://example.com/dashboard'
        )

        self.cli.publish(
            'smtp://mailhog:1025/welcome',
            {
                'to': user_data['email'],
                'subject': f'Welcome to Our Service, {user_data["name"]}!',
                'html': html_content
            }
        )

    def send_alert(self, alert_data):
        template = self.jinja_env.get_template('alert.html')
        
        # Set alert color based on priority
        colors = {
            'high': '#dc3545',
            'medium': '#ffc107',
            'low': '#17a2b8'
        }
        
        html_content = template.render(
            alert_type=alert_data['type'],
            alert_color=colors[alert_data['priority']],
            alert_title=alert_data['title'],
            alert_message=alert_data['message'],
            priority=alert_data['priority'],
            timestamp=datetime.now().isoformat(),
            system_name=alert_data['system'],
            component=alert_data['component'],
            action_required=alert_data.get('action_required', False),
            action_description=alert_data.get('action_description', ''),
            action_url=alert_data.get('action_url', '')
        )

        self.cli.publish(
            'smtp://mailhog:1025/alert',
            {
                'to': alert_data['recipient'],
                'subject': f'System Alert: {alert_data["title"]}',
                'html': html_content
            }
        )

    def send_daily_digest(self, user_email):
        template = self.jinja_env.get_template('digest.html')
        
        # Simulate daily metrics
        activities = [
            {
                'time': (datetime.now() - timedelta(hours=i)).strftime('%H:%M'),
                'description': f'Activity {i+1} description'
            } for i in range(5)
        ]

        upcoming_events = [
            {
                'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'name': f'Event {i+1}'
            } for i in range(3)
        ]

        html_content = template.render(
            date=datetime.now().strftime('%Y-%m-%d'),
            active_users=random.randint(100, 1000),
            new_signups=random.randint(10, 50),
            total_interactions=random.randint(1000, 5000),
            activities=activities,
            avg_response_time=random.randint(50, 200),
            uptime='99.99%',
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            upcoming_events=upcoming_events,
            dashboard_url='https://example.com/dashboard'
        )

        self.cli.publish(
            'smtp://mailhog:1025/digest',
            {
                'to': user_email,
                'subject': f'Daily Digest - {datetime.now().strftime("%Y-%m-%d")}',
                'html': html_content
            }
        )

    def simulate_notifications(self):
        print("Starting Email Notification System simulation...")
        
        # Simulate users
        users = [
            {
                'name': f'User {i}',
                'username': f'user{i}',
                'email': f'user{i}@example.com'
            } for i in range(1, 6)
        ]

        # Simulate alert types
        alert_types = ['Security', 'Performance', 'System Update', 'Maintenance']
        components = ['Database', 'API', 'Frontend', 'Backend']
        priorities = ['high', 'medium', 'low']

        while True:
            try:
                # Simulate new user registration
                if random.random() < 0.3:  # 30% chance
                    user = random.choice(users)
                    print(f"Sending welcome email to {user['email']}")
                    self.send_welcome_email(user)

                # Simulate system alerts
                if random.random() < 0.4:  # 40% chance
                    alert_data = {
                        'type': random.choice(alert_types),
                        'priority': random.choice(priorities),
                        'title': 'System Alert Title',
                        'message': 'Detailed alert message goes here.',
                        'system': 'Production',
                        'component': random.choice(components),
                        'recipient': random.choice(users)['email'],
                        'action_required': random.choice([True, False])
                    }
                    if alert_data['action_required']:
                        alert_data.update({
                            'action_description': 'Action needed to resolve the alert',
                            'action_url': 'https://example.com/alerts/action'
                        })
                    print(f"Sending alert: {alert_data['title']}")
                    self.send_alert(alert_data)

                # Simulate daily digest
                current_hour = datetime.now().hour
                if current_hour == 9:  # Send digest at 9 AM
                    for user in users:
                        print(f"Sending daily digest to {user['email']}")
                        self.send_daily_digest(user['email'])

                time.sleep(10)  # Wait 10 seconds between simulations

            except Exception as e:
                print(f"Error in simulation: {e}")
                time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    notification_system = EmailNotificationSystem()
    notification_system.simulate_notifications()
