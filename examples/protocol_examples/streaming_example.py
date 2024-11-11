"""
Example demonstrating streaming protocol endpoints (RTSP, HLS, DASH)
"""
from uripoint import UriPointCLI

def setup_streaming_endpoints():
    cli = UriPointCLI()

    # RTSP endpoint for a security camera
    cli.create_endpoint(
        uri='rtsp://localhost:8554/camera1',
        data={
            'stream_url': 'rtsp://camera.example.com/stream1',
            'transport': 'tcp',
            'auth': {
                'username': 'admin',
                'password': 'secure123'
            },
            'options': {
                'latency': 100,
                'buffer_size': 2048
            }
        }
    )

    # HLS endpoint for live streaming
    cli.create_endpoint(
        uri='http://localhost:8080/live/stream.m3u8',
        data={
            'manifest_url': '/live/stream.m3u8',
            'segment_duration': 6,
            'playlist_size': 5,
            'options': {
                'encryption': True,
                'key_rotation': 300,
                'bandwidth_variants': [
                    {'resolution': '1080p', 'bitrate': 5000000},
                    {'resolution': '720p', 'bitrate': 2500000},
                    {'resolution': '480p', 'bitrate': 1000000}
                ]
            }
        }
    )

    # DASH endpoint for video on demand
    cli.create_endpoint(
        uri='http://localhost:8080/vod/manifest.mpd',
        data={
            'mpd_url': '/vod/manifest.mpd',
            'segment_duration': 4,
            'options': {
                'min_buffer': 8,
                'max_buffer': 30,
                'quality_levels': [
                    {'resolution': '2160p', 'bitrate': 15000000},
                    {'resolution': '1440p', 'bitrate': 8000000},
                    {'resolution': '1080p', 'bitrate': 4500000},
                    {'resolution': '720p', 'bitrate': 2500000}
                ],
                'audio_tracks': [
                    {'language': 'eng', 'channels': '5.1'},
                    {'language': 'eng', 'channels': '2.0'},
                    {'language': 'spa', 'channels': '2.0'}
                ]
            }
        }
    )

    print("\nStreaming endpoints created:")
    print("1. RTSP Camera Stream:")
    print("   - URL: rtsp://localhost:8554/camera1")
    print("   - Transport: TCP")
    print("   - Type: Live Security Camera Feed")
    
    print("\n2. HLS Live Stream:")
    print("   - URL: http://localhost:8080/live/stream.m3u8")
    print("   - Segment Duration: 6 seconds")
    print("   - Quality Variants: 1080p, 720p, 480p")
    
    print("\n3. DASH Video on Demand:")
    print("   - URL: http://localhost:8080/vod/manifest.mpd")
    print("   - Segment Duration: 4 seconds")
    print("   - Quality Levels: 2160p to 720p")
    print("   - Audio: 5.1 and 2.0 channels, multiple languages")

def test_streaming_endpoints():
    """
    Example of how to interact with streaming endpoints
    """
    cli = UriPointCLI()

    # Test RTSP endpoint
    rtsp_response = cli.get_endpoint('rtsp://localhost:8554/camera1')
    if rtsp_response:
        print("\nRTSP Camera Status:")
        print(f"Stream URL: {rtsp_response.get('config', {}).get('stream_url')}")
        print(f"Transport: {rtsp_response.get('config', {}).get('transport')}")

    # Test HLS endpoint
    hls_response = cli.get_endpoint('http://localhost:8080/live/stream.m3u8')
    if hls_response:
        print("\nHLS Stream Status:")
        config = hls_response.get('config', {})
        print(f"Manifest: {config.get('manifest_url')}")
        print(f"Segment Duration: {config.get('segment_duration')}s")
        variants = config.get('options', {}).get('bandwidth_variants', [])
        print(f"Available Qualities: {[v['resolution'] for v in variants]}")

    # Test DASH endpoint
    dash_response = cli.get_endpoint('http://localhost:8080/vod/manifest.mpd')
    if dash_response:
        print("\nDASH Stream Status:")
        config = dash_response.get('config', {})
        print(f"MPD URL: {config.get('mpd_url')}")
        print(f"Segment Duration: {config.get('segment_duration')}s")
        qualities = config.get('options', {}).get('quality_levels', [])
        print(f"Available Qualities: {[q['resolution'] for q in qualities]}")

if __name__ == '__main__':
    print("Setting up streaming protocol endpoints...")
    setup_streaming_endpoints()
    
    print("\nTesting streaming endpoints...")
    test_streaming_endpoints()
