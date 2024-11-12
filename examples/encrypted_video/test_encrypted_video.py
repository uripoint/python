"""
Test script for encrypted video streaming endpoints
"""
import requests
import time
import subprocess
import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from config import ENDPOINTS, KEY_DIR, TEMP_DIR

class StreamTester:
    def __init__(self):
        self.key_dir = Path(__file__).parent / KEY_DIR
        self.temp_dir = Path(__file__).parent / TEMP_DIR
        self.temp_dir.mkdir(exist_ok=True)

    def load_key(self, key_file):
        """Load encryption key"""
        with open(self.key_dir / key_file, 'rb') as f:
            return f.read()

    def test_hls_encryption(self):
        """Test HLS encryption"""
        print("\nTesting HLS encryption...")
        
        # Get master playlist
        response = requests.get(ENDPOINTS['hls_master'])
        assert response.status_code == 200, "Failed to get HLS master playlist"
        master_content = response.text
        print("Master playlist:", master_content)

        # Check for encryption info
        assert '#EXT-X-KEY' in master_content, "No encryption info in playlist"

        # Get encryption key
        key_url = next(line.split('URI="')[1].split('"')[0] 
                      for line in master_content.split('\n') 
                      if '#EXT-X-KEY' in line)
        key_response = requests.get(key_url)
        assert key_response.status_code == 200, "Failed to get encryption key"
        
        # Verify key format
        key = base64.b64decode(key_response.text)
        assert len(key) == 16, "Invalid key length"

        print("HLS encryption verified")
        return True

    def test_dash_encryption(self):
        """Test DASH encryption"""
        print("\nTesting DASH encryption...")
        
        # Get manifest
        response = requests.get(ENDPOINTS['dash_manifest'])
        assert response.status_code == 200, "Failed to get DASH manifest"
        manifest = response.text
        print("DASH manifest:", manifest)

        # Check for encryption info
        assert 'ContentProtection' in manifest, "No encryption info in manifest"
        assert 'cenc:default_KID' in manifest, "No KID in manifest"

        # Test license server
        license_data = {
            'kids': [manifest.split('default_KID="')[1].split('"')[0]]
        }
        license_response = requests.post(
            ENDPOINTS['drm_license'],
            json=license_data
        )
        assert license_response.status_code == 200, "Failed to get license"
        
        # Verify license format
        license_info = license_response.json()
        assert 'keys' in license_info, "No keys in license"
        assert len(license_info['keys']) > 0, "Empty license keys"

        print("DASH encryption verified")
        return True

    def test_key_rotation(self):
        """Test key rotation"""
        print("\nTesting key rotation...")
        
        # Get key management info
        response = requests.get(ENDPOINTS['key_manage'])
        assert response.status_code == 200, "Failed to get key management info"
        key_info = response.json()
        
        # Verify key management structure
        assert 'rotation_interval' in key_info, "No rotation interval"
        assert 'active_keys' in key_info, "No active keys list"
        assert 'revoked_keys' in key_info, "No revoked keys list"

        print("Key rotation mechanism verified")
        return True

    def verify_encrypted_segment(self, segment_url, key):
        """Verify an encrypted segment"""
        print(f"\nVerifying encrypted segment: {segment_url}")
        
        # Download segment
        response = requests.get(segment_url)
        assert response.status_code == 200, "Failed to get segment"
        
        # Save encrypted segment
        segment_path = self.temp_dir / 'test_segment.ts'
        with open(segment_path, 'wb') as f:
            f.write(response.content)
        
        # Use ffprobe to check segment
        probe_result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type',
             '-of', 'json', str(segment_path)],
            capture_output=True, text=True
        )
        
        # Clean up
        segment_path.unlink()
        
        assert probe_result.returncode == 0, "Failed to probe segment"
        return True

    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir.exists():
            for file in self.temp_dir.glob('*'):
                file.unlink()
            self.temp_dir.rmdir()

def main():
    """Main test function"""
    tester = StreamTester()
    try:
        # Test all encryption mechanisms
        assert tester.test_hls_encryption(), "HLS encryption test failed"
        assert tester.test_dash_encryption(), "DASH encryption test failed"
        assert tester.test_key_rotation(), "Key rotation test failed"
        
        print("\nAll encryption tests passed!")
        
    except AssertionError as e:
        print(f"\nTest failed: {str(e)}")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        tester.cleanup()

if __name__ == '__main__':
    main()
