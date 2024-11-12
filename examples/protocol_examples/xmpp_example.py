"""
Example demonstrating XMPP protocol support in UriPoint
"""
from uripoint import UriPointCLI

def setup_xmpp_endpoints():
    """Setup XMPP messaging endpoints"""
    cli = UriPointCLI()

    # XMPP server endpoint
    cli.create_endpoint(
        uri='xmpp://localhost:5222/server',
        data={
            'server_config': {
                'domain': 'chat.example.com',
                'tls': True,
                'auth_methods': ['PLAIN', 'DIGEST-MD5', 'SCRAM-SHA-1'],
                'max_clients': 1000,
                'features': [
                    'jabber:iq:roster',
                    'jabber:iq:privacy',
                    'urn:xmpp:ping',
                    'urn:xmpp:mam:2'
                ]
            }
        }
    )

    # Chat room service
    cli.create_endpoint(
        uri='xmpp://localhost:5222/muc.chat.example.com',
        data={
            'service_type': 'conference',
            'features': {
                'muc_passwordprotected': True,
                'muc_hidden': False,
                'muc_temporary': False,
                'muc_open': True,
                'muc_moderated': True,
                'muc_persistent': True
            },
            'default_config': {
                'max_users': 100,
                'members_only': False,
                'allow_private_messages': True,
                'allow_invites': True
            }
        }
    )

    # File transfer proxy
    cli.create_endpoint(
        uri='xmpp://localhost:5222/proxy.chat.example.com',
        data={
            'service_type': 'proxy',
            'features': {
                'http_upload': True,
                'socks5': True,
                'ibb': True
            },
            'upload_limits': {
                'max_file_size': 10485760,  # 10MB
                'allowed_types': ['image/*', 'audio/*', 'video/*', 'application/pdf']
            }
        }
    )

    # PubSub service
    cli.create_endpoint(
        uri='xmpp://localhost:5222/pubsub.chat.example.com',
        data={
            'service_type': 'pubsub',
            'features': {
                'persistent-items': True,
                'create-nodes': True,
                'delete-nodes': True,
                'publish-options': True,
                'subscribe': True
            },
            'node_config': {
                'max_items': 1000,
                'notify_retract': True,
                'notify_delete': True,
                'persist_items': True
            }
        }
    )

    # User status service
    cli.create_endpoint(
        uri='xmpp://localhost:5222/status.chat.example.com',
        data={
            'service_type': 'presence',
            'features': {
                'last_activity': True,
                'user_mood': True,
                'user_tune': True,
                'user_location': True
            }
        }
    )

    print("\nXMPP endpoints created:")
    print("1. XMPP Server:")
    print("   - URI: xmpp://localhost:5222/server")
    print("   - Domain: chat.example.com")
    print("   - Features: roster, privacy, ping, mam")
    
    print("\n2. Chat Rooms:")
    print("   - URI: xmpp://localhost:5222/muc.chat.example.com")
    print("   - Type: Multi-User Chat")
    print("   - Features: password protection, moderation")
    
    print("\n3. File Transfer:")
    print("   - URI: xmpp://localhost:5222/proxy.chat.example.com")
    print("   - Features: HTTP upload, SOCKS5, IBB")
    
    print("\n4. PubSub Service:")
    print("   - URI: xmpp://localhost:5222/pubsub.chat.example.com")
    print("   - Features: persistent items, node management")

def test_xmpp_features():
    """Test XMPP protocol features"""
    cli = UriPointCLI()

    # Create chat room
    print("\nCreating chat room...")
    room_config = {
        'room': 'development',
        'name': 'Development Team',
        'description': 'Development team chat room',
        'password': 'secret123',
        'max_users': 50
    }
    cli.publish('xmpp://localhost:5222/muc.chat.example.com', room_config)

    # Send message to room
    print("\nSending message to room...")
    message = {
        'to': 'development@muc.chat.example.com',
        'type': 'groupchat',
        'body': 'Hello team!',
        'subject': 'Daily Update'
    }
    cli.publish('xmpp://localhost:5222/server', message)

    # Create PubSub node
    print("\nCreating PubSub node...")
    node_config = {
        'node': 'team_updates',
        'title': 'Team Updates',
        'access_model': 'whitelist',
        'publish_model': 'publishers'
    }
    cli.publish('xmpp://localhost:5222/pubsub.chat.example.com', node_config)

    # Upload file
    print("\nUploading file...")
    file_data = {
        'name': 'document.pdf',
        'size': 1024,
        'type': 'application/pdf',
        'content': 'base64_encoded_content'
    }
    cli.publish('xmpp://localhost:5222/proxy.chat.example.com', file_data)

    # Update user status
    print("\nUpdating user status...")
    status_data = {
        'show': 'dnd',
        'status': 'In a meeting',
        'priority': 5,
        'mood': 'busy',
        'location': {
            'description': 'Office',
            'lat': 37.7749,
            'lon': -122.4194
        }
    }
    cli.publish('xmpp://localhost:5222/status.chat.example.com', status_data)

def setup_xmpp_options():
    """Configure XMPP protocol options"""
    return {
        'security': {
            'tls': True,
            'verify_cert': True,
            'allow_insecure': False,
            'cert_file': '/path/to/cert.pem',
            'key_file': '/path/to/key.pem'
        },
        'connection': {
            'keepalive': 60,
            'reconnect': True,
            'reconnect_delay': 5,
            'max_reconnects': 10
        },
        'stanza': {
            'timeout': 30,
            'max_size': 65535,
            'queue_size': 1000
        }
    }

if __name__ == '__main__':
    print("Setting up XMPP endpoints...")
    setup_xmpp_endpoints()
    
    print("\nTesting XMPP features...")
    test_xmpp_features()
