"""
Test script for video streaming endpoints
"""
import requests
import time
import subprocess
import json
from pathlib import Path

def test_endpoint(url, expected_content_type=None, save_output=False):
    """Test an endpoint and optionally save its output"""
    print(f"\nTesting {url}")
    try:
        response = requests.get(url, stream=True)
        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('Content-Type')}")
        
        if expected_content_type:
            assert response.headers.get('Content-Type').startswith(expected_content_type), \
                f"Expected content type {expected_content_type}, got {response.headers.get('Content-Type')}"
        
        if save_output:
            output_file = Path(f"test_output_{int(time.time())}.ts")
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Saved output to {output_file}")
            
            # Verify file with ffprobe
            probe_result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height', 
                 '-of', 'json', str(output_file)],
                capture_output=True, text=True
            )
            if probe_result.returncode == 0:
                streams = json.loads(probe_result.stdout)
                print("Stream information:")
                print(json.dumps(streams, indent=2))
            else:
                print("Failed to probe output file")
            
            # Cleanup
            output_file.unlink()
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_hls_stream():
    """Test HLS streaming"""
    print("\nTesting HLS stream...")
    
    # Test master playlist
    master_url = "http://localhost:8000/hls/master.m3u8"
    response = requests.get(master_url)
    assert response.status_code == 200, "Failed to get master playlist"
    assert "#EXTM3U" in response.text, "Invalid master playlist"
    
    # Parse and test variant streams
    variants = [line for line in response.text.split('\n') if line.endswith('.m3u8')]
    for variant in variants:
        variant_url = f"http://localhost:8000/hls/{variant}"
        print(f"\nTesting variant: {variant_url}")
        response = requests.get(variant_url)
        assert response.status_code == 200, f"Failed to get variant playlist: {variant}"
        assert "#EXTM3U" in response.text, f"Invalid variant playlist: {variant}"

def test_dash_stream():
    """Test DASH streaming"""
    print("\nTesting DASH stream...")
    
    # Test manifest
    manifest_url = "http://localhost:8000/dash/manifest.mpd"
    response = requests.get(manifest_url)
    assert response.status_code == 200, "Failed to get DASH manifest"
    assert 'MPD' in response.text, "Invalid DASH manifest"

def test_status_endpoint():
    """Test status endpoint"""
    print("\nTesting status endpoint...")
    
    response = requests.get("http://localhost:8000/status")
    assert response.status_code == 200, "Failed to get status"
    
    status = response.json()
    print("Stream status:")
    print(json.dumps(status, indent=2))
    
    assert 'streams' in status, "Missing streams in status"
    assert 'viewers' in status, "Missing viewers in status"

def main():
    """Main test function"""
    try:
        # Test direct video endpoints
        test_endpoint("http://localhost:8000/video/test", "video/MP2T", save_output=True)
        test_endpoint("http://localhost:8000/video/webcam", "video/MP2T")
        
        # Test streaming protocols
        test_hls_stream()
        test_dash_stream()
        
        # Test status
        test_status_endpoint()
        
        print("\nAll tests completed successfully!")
        
    except AssertionError as e:
        print(f"\nTest failed: {str(e)}")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == '__main__':
    main()
