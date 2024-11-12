"""
Redis Session Manager and Notification System using UriPoint
"""

from uripoint import UriPointCLI
import json
import time
import random
from datetime import datetime
import uuid

class SessionManager:
    def __init__(self):
        self.cli = UriPointCLI()
        self.setup_endpoints()
        self.session_ttl = 3600  # 1 hour session timeout
        self.rate_limit_window = 60  # 1 minute window for rate limiting
        self.rate_limit_max = 100  # max requests per window

    def setup_endpoints(self):
        # Session management endpoints
        self.cli.create_endpoint(
            uri='redis://redis:6379/sessions/{user_id}',
            data={
                'type': 'hash',
                'ttl': self.session_ttl
            }
        )

        # Notification channel endpoints
        self.cli.create_endpoint(
            uri='redis://redis:6379/notifications/{user_id}',
            data={
                'type': 'pubsub'
            }
        )

        # User presence endpoints
        self.cli.create_endpoint(
            uri='redis://redis:6379/presence/{user_id}',
            data={
                'type': 'string',
                'ttl': 300  # 5 minutes presence timeout
            }
        )

        # Rate limiting endpoints
        self.cli.create_endpoint(
            uri='redis://redis:6379/ratelimit/{api_key}',
            data={
                'type': 'string',
                'ttl': self.rate_limit_window
            }
        )

    def create_session(self, user_id):
        session_data = {
            'session_id': str(uuid.uuid4()),
            'created_at': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
            'user_agent': 'Python/3.9',
            'ip_address': f'192.168.1.{random.randint(2, 254)}'
        }

        self.cli.publish(
            f'redis://redis:6379/sessions/{user_id}',
            session_data
        )
        return session_data['session_id']

    def update_presence(self, user_id, status='online'):
        presence_data = {
            'status': status,
            'last_seen': datetime.now().isoformat(),
            'device': 'web'
        }

        self.cli.publish(
            f'redis://redis:6379/presence/{user_id}',
            presence_data
        )

    def send_notification(self, user_id, notification_type, message):
        notification = {
            'id': str(uuid.uuid4()),
            'type': notification_type,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

        self.cli.publish(
            f'redis://redis:6379/notifications/{user_id}',
            notification
        )

    def check_rate_limit(self, api_key):
        current_count = self.cli.get(f'redis://redis:6379/ratelimit/{api_key}')
        count = int(current_count) if current_count else 0

        if count >= self.rate_limit_max:
            return False

        self.cli.publish(
            f'redis://redis:6379/ratelimit/{api_key}',
            str(count + 1)
        )
        return True

    def simulate_user_activity(self):
        # Simulate multiple users
        users = [f'user_{i}' for i in range(1, 6)]
        api_keys = [f'api_key_{i}' for i in range(1, 4)]

        while True:
            try:
                # Simulate user sessions and presence
                for user_id in users:
                    if random.random() < 0.3:  # 30% chance of session creation
                        session_id = self.create_session(user_id)
                        print(f"Created session {session_id} for {user_id}")

                    # Update user presence
                    status = random.choice(['online', 'away', 'busy'])
                    self.update_presence(user_id, status)

                    # Simulate notifications
                    if random.random() < 0.4:  # 40% chance of notification
                        notification_type = random.choice([
                            'message', 'friend_request', 'system_alert'
                        ])
                        message = f"Test notification for {user_id}"
                        self.send_notification(user_id, notification_type, message)
                        print(f"Sent {notification_type} notification to {user_id}")

                # Simulate API rate limiting
                for api_key in api_keys:
                    # Simulate API calls
                    for _ in range(random.randint(10, 30)):
                        if self.check_rate_limit(api_key):
                            print(f"API call allowed for {api_key}")
                        else:
                            print(f"Rate limit exceeded for {api_key}")

                time.sleep(2)  # Wait before next simulation cycle

            except Exception as e:
                print(f"Error in simulation: {e}")
                time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    manager = SessionManager()
    print("Starting Session Manager simulation...")
    manager.simulate_user_activity()
