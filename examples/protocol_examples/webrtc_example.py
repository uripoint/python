"""
Example demonstrating WebRTC protocol support in UriPoint
"""
from uripoint import UriPointCLI

def setup_webrtc_endpoints():
    """Setup WebRTC communication endpoints"""
    cli = UriPointCLI()

    # Signaling server endpoint
    cli.create_endpoint(
        uri='ws://localhost:8080/webrtc/signal',
        data={
            'service_type': 'signaling',
            'features': {
                'ice': True,
                'sdp': True,
                'data_channel': True,
                'media_relay': True
            },
            'ice_servers': [
                {
                    'urls': ['stun:stun.example.com:19302']
                },
                {
                    'urls': ['turn:turn.example.com:3478'],
                    'username': 'webrtc',
                    'credential': 'turnserver'
                }
            ],
            'options': {
                'max_clients': 1000,
                'timeout': 30,
                'ping_interval': 5
            }
        }
    )

    # Video room service
    cli.create_endpoint(
        uri='webrtc://localhost:8080/rooms',
        data={
            'service_type': 'conference',
            'features': {
                'video': True,
                'audio': True,
                'screen_share': True,
                'recording': True
            },
            'media_config': {
                'video': {
                    'codecs': ['VP8', 'VP9', 'H264'],
                    'resolutions': ['1080p', '720p', '480p'],
                    'framerates': [30, 24, 15],
                    'bitrates': {
                        'min': 100000,
                        'max': 4000000
                    }
                },
                'audio': {
                    'codecs': ['opus', 'G722'],
                    'channels': [1, 2],
                    'bitrates': {
                        'min': 8000,
                        'max': 128000
                    }
                }
            },
            'room_config': {
                'max_participants': 12,
                'record': True,
                'chat': True,
                'moderation': True
            }
        }
    )

    # Data channel service
    cli.create_endpoint(
        uri='webrtc://localhost:8080/data',
        data={
            'service_type': 'datachannel',
            'features': {
                'reliable': True,
                'ordered': True,
                'max_retransmits': 3
            },
            'channels': {
                'chat': {
                    'ordered': True,
                    'maxPacketLifeTime': 1000
                },
                'file': {
                    'ordered': True,
                    'protocol': 'binary'
                },
                'game': {
                    'ordered': False,
                    'maxRetransmits': 0
                }
            }
        }
    )

    # Recording service
    cli.create_endpoint(
        uri='webrtc://localhost:8080/recording',
        data={
            'service_type': 'recording',
            'features': {
                'formats': ['webm', 'mp4'],
                'compositing': True,
                'transcoding': True
            },
            'storage': {
                'type': 's3',
                'bucket': 'recordings',
                'retention': '30d'
            },
            'options': {
                'auto_start': True,
                'split_participants': True,
                'max_duration': 7200
            }
        }
    )

    print("\nWebRTC endpoints created:")
    print("1. Signaling Server:")
    print("   - URI: ws://localhost:8080/webrtc/signal")
    print("   - Features: ICE, SDP, Data Channel")
    print("   - STUN/TURN support")
    
    print("\n2. Video Rooms:")
    print("   - URI: webrtc://localhost:8080/rooms")
    print("   - Features: Video, Audio, Screen Share")
    print("   - Codecs: VP8, VP9, H264, opus")
    
    print("\n3. Data Channels:")
    print("   - URI: webrtc://localhost:8080/data")
    print("   - Channels: chat, file, game")
    print("   - Features: Reliable, Ordered delivery")
    
    print("\n4. Recording:")
    print("   - URI: webrtc://localhost:8080/recording")
    print("   - Formats: WebM, MP4")
    print("   - Features: Compositing, Transcoding")

def test_webrtc_features():
    """Test WebRTC protocol features"""
    cli = UriPointCLI()

    # Create video room
    print("\nCreating video room...")
    room_config = {
        'name': 'team_meeting',
        'type': 'conference',
        'max_participants': 8,
        'features': {
            'video': True,
            'audio': True,
            'screen_share': True,
            'recording': True
        }
    }
    cli.publish('webrtc://localhost:8080/rooms', room_config)

    # Send signaling message
    print("\nSending signaling message...")
    signal = {
        'type': 'offer',
        'sdp': 'v=0\r\no=- 123456 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\n...',
        'room': 'team_meeting',
        'peer_id': 'user123'
    }
    cli.publish('ws://localhost:8080/webrtc/signal', signal)

    # Create data channel
    print("\nCreating data channel...")
    channel_config = {
        'name': 'chat',
        'ordered': True,
        'maxPacketLifeTime': 1000,
        'protocol': 'json'
    }
    cli.publish('webrtc://localhost:8080/data', channel_config)

    # Start recording
    print("\nStarting recording...")
    recording_config = {
        'room': 'team_meeting',
        'format': 'webm',
        'options': {
            'video_codec': 'VP8',
            'audio_codec': 'opus',
            'composite': True
        }
    }
    cli.publish('webrtc://localhost:8080/recording', recording_config)

def setup_webrtc_options():
    """Configure WebRTC protocol options"""
    return {
        'media': {
            'video': {
                'mandatory': {
                    'maxWidth': 1920,
                    'maxHeight': 1080,
                    'maxFrameRate': 30
                },
                'optional': [
                    {'minWidth': 640},
                    {'minHeight': 480}
                ]
            },
            'audio': {
                'mandatory': {
                    'echoCancellation': True,
                    'noiseSuppression': True
                }
            }
        },
        'peer': {
            'iceTransportPolicy': 'all',
            'bundlePolicy': 'max-bundle',
            'rtcpMuxPolicy': 'require',
            'iceCandidatePoolSize': 10
        },
        'signaling': {
            'reconnectInterval': 3000,
            'maxRetries': 5,
            'pingTimeout': 5000
        }
    }

if __name__ == '__main__':
    print("Setting up WebRTC endpoints...")
    setup_webrtc_endpoints()
    
    print("\nTesting WebRTC features...")
    test_webrtc_features()
