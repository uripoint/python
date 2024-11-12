"""
Test script for security features
"""
import requests
import json
import jwt
import ssl
import websockets
import asyncio
import time
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.backends import default_backend

class SecurityTester:
    def __init__(self):
        self.base_url = "https://localhost:8000"
        self.ssl_dir = Path(__file__).parent / 'ssl'
        self.session = requests.Session()
        self.session.verify = str(self.ssl_dir / 'cert.pem')

    def test_input_validation(self):
        """Test input validation endpoint"""
        print("\nTesting input validation...")
        
        # Test valid input
        valid_data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "SecurePass123"
        }
        response = self.session.post(f"{self.base_url}/validate", json=valid_data)
        assert response.status_code == 200, "Valid input validation failed"
        
        # Test invalid input
        invalid_data = {
            "username": "te",  # Too short
            "email": "invalid-email",
            "password": "short"
        }
        response = self.session.post(f"{self.base_url}/validate", json=invalid_data)
        assert response.status_code == 400, "Invalid input validation failed"
        
        print("Input validation tests passed")

    def test_authentication(self):
        """Test authentication endpoint"""
        print("\nTesting authentication...")
        
        # Test token generation
        auth_data = {
            "username": "testuser",
            "password": "testpass"
        }
        response = self.session.post(f"{self.base_url}/auth/token", json=auth_data)
        assert response.status_code == 200, "Token generation failed"
        token = response.json().get('token')
        assert token, "No token in response"
        
        # Verify token
        decoded = jwt.decode(token, options={"verify_signature": False})
        assert 'exp' in decoded, "No expiration in token"
        
        print("Authentication tests passed")

    def test_process_security(self):
        """Test process management security"""
        print("\nTesting process management security...")
        
        # Test allowed process
        process_data = {
            "command": "ffmpeg",
            "args": ["-version"]
        }
        response = self.session.post(f"{self.base_url}/process/manage", json=process_data)
        assert response.status_code == 200, "Allowed process failed"
        
        # Test blocked process
        process_data = {
            "command": "rm",
            "args": ["-rf", "/"]
        }
        response = self.session.post(f"{self.base_url}/process/manage", json=process_data)
        assert response.status_code == 403, "Blocked process not prevented"
        
        print("Process security tests passed")

    def test_network_security(self):
        """Test network security features"""
        print("\nTesting network security...")
        
        # Test rate limiting
        start_time = time.time()
        requests_count = 0
        for _ in range(150):  # Try to exceed rate limit
            response = self.session.get(f"{self.base_url}/security/network")
            if response.status_code == 429:  # Rate limit reached
                break
            requests_count += 1
        
        assert requests_count < 150, "Rate limiting not working"
        
        # Test firewall rules
        response = self.session.get(f"{self.base_url}/security/network")
        assert 'X-RateLimit-Remaining' in response.headers, "Rate limit headers missing"
        
        print("Network security tests passed")

    async def test_websocket_security(self):
        """Test WebSocket security"""
        print("\nTesting WebSocket security...")
        
        ssl_context = ssl.create_default_context(cafile=str(self.ssl_dir / 'cert.pem'))
        
        try:
            async with websockets.connect(
                f"wss://localhost:8000/security/ws",
                ssl=ssl_context
            ) as websocket:
                # Test message validation
                await websocket.send(json.dumps({"type": "test", "data": "valid"}))
                response = await websocket.recv()
                assert response, "No response from WebSocket"
                
                # Test invalid message
                try:
                    await websocket.send("invalid json")
                    response = await websocket.recv()
                    assert 'error' in response, "Invalid message not rejected"
                except websockets.exceptions.ConnectionClosed:
                    pass  # Expected behavior
        except Exception as e:
            assert False, f"WebSocket test failed: {str(e)}"
        
        print("WebSocket security tests passed")

    def test_tls_configuration(self):
        """Test TLS configuration"""
        print("\nTesting TLS configuration...")
        
        # Test TLS version
        response = self.session.get(f"{self.base_url}/security/tls")
        assert response.status_code == 200, "TLS endpoint failed"
        
        # Verify certificate
        cert_path = self.ssl_dir / 'cert.pem'
        with open(cert_path, 'rb') as f:
            cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
        assert cert.version == x509.Version.v3, "Invalid certificate version"
        
        # Test HSTS
        assert 'Strict-Transport-Security' in response.headers, "HSTS not enabled"
        
        print("TLS configuration tests passed")

    def test_security_monitoring(self):
        """Test security monitoring"""
        print("\nTesting security monitoring...")
        
        response = self.session.get(f"{self.base_url}/security/monitor")
        assert response.status_code == 200, "Monitoring endpoint failed"
        
        data = response.json()
        assert 'metrics' in data, "No metrics in monitoring data"
        assert 'alerts' in data, "No alerts in monitoring data"
        
        print("Security monitoring tests passed")

def main():
    """Main test function"""
    tester = SecurityTester()
    try:
        # Run synchronous tests
        tester.test_input_validation()
        tester.test_authentication()
        tester.test_process_security()
        tester.test_network_security()
        tester.test_tls_configuration()
        tester.test_security_monitoring()
        
        # Run asynchronous tests
        asyncio.get_event_loop().run_until_complete(tester.test_websocket_security())
        
        print("\nAll security tests passed!")
        
    except AssertionError as e:
        print(f"\nTest failed: {str(e)}")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == '__main__':
    main()
