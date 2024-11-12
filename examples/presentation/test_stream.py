"""
Test script for video streaming functionality
"""
import subprocess
import time
import requests
import json
import os
from pathlib import Path

def create_test_video():
    """Create a test video file using ffmpeg"""
    print("Creating test video...")
    
    # Create test video with color bars and time overlay
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'testsrc=duration=30:size=1280x720:rate=30',
        '-f', 'lavfi', '-i', 'sine=frequency=1000:duration=30',
        '-vf', 'drawtext=text=\'%{pts\\:hms}\':box=1:x=(w-tw)/2:y=h-(2*lh):fontsize=72',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '3000k',
        '-c:a', 'aac', '-b:a', '128k',
        'test_video.mp4'
    ]
    
    subprocess.run(cmd, check=True)
    return Path('test_video.mp4').absolute()

def setup_streaming_server(video_path):
    """Setup streaming server with test video"""
    print("Setting up streaming server...")
    
    # Start ffmpeg to create HLS stream
    cmd = [
        'ffmpeg', '-y', '-re',
        '-i', str(video_path),
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-f', 'hls',
        '-hls_time', '4',
        '-hls_list_size', '5',
        '-hls_flags', 'delete_segments',
        'stream.m3u8'
    ]
    
    ffmpeg_process = subprocess.Popen(cmd)
    return ffmpeg_process

def test_hls_endpoint():
    """Test HLS endpoint"""
    print("Testing HLS endpoint...")
    
    # Test manifest
    response = requests.get('http://localhost:8080/live/stream.m3u8')
    assert response.status_code == 200, "Failed to get HLS manifest"
    assert '#EXTM3U' in response.text, "Invalid HLS manifest"
    
    # Test segments
    manifest_lines = response.text.split('\n')
    segment_urls = [line for line in manifest_lines if line.endswith('.ts')]
    assert len(segment_urls) > 0, "No segments found in manifest"
    
    # Test segment download
    for segment in segment_urls[:1]:  # Test first segment
        response = requests.get(f'http://localhost:8080/live/{segment}')
        assert response.status_code == 200, f"Failed to get segment: {segment}"
        assert len(response.content) > 0, f"Empty segment: {segment}"

def test_stream_status():
    """Test stream status endpoint"""
    print("Testing status endpoint...")
    
    response = requests.get('http://localhost:8080/api/stream/status')
    assert response.status_code == 200, "Failed to get stream status"
    
    status = response.json()
    assert status['status'] == 'live', "Stream not live"
    assert 'viewers' in status, "Missing viewers count"
    assert 'quality' in status, "Missing quality info"

def main():
    """Main test function"""
    try:
        # Create test video
        video_path = create_test_video()
        print(f"Test video created: {video_path}")

        # Setup streaming
        ffmpeg_process = setup_streaming_server(video_path)
        print("Streaming server started")

        # Wait for stream to initialize
        time.sleep(5)

        # Run tests
        test_hls_endpoint()
        test_stream_status()

        print("\nAll tests passed!")

    except AssertionError as e:
        print(f"\nTest failed: {str(e)}")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        # Cleanup
        if 'ffmpeg_process' in locals():
            ffmpeg_process.terminate()
            ffmpeg_process.wait()
        if os.path.exists('test_video.mp4'):
            os.remove('test_video.mp4')
        if os.path.exists('stream.m3u8'):
            os.remove('stream.m3u8')
        for f in Path('.').glob('*.ts'):
            f.unlink()

if __name__ == '__main__':
    main()
