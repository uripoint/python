import pytest
from uripoint.main import UriPointCLI
import os
import tempfile
import yaml
import json

class TestUriPointCLI:
    def setup_method(self):
        """Setup method to create a fresh CLI instance with a temporary config file for each test"""
        self.cli = UriPointCLI()
        self.original_config_file = self.cli.config_file
        self.temp_config_file = os.path.join(tempfile.gettempdir(), f'test_uripoint_config_{os.getpid()}.yaml')
        self.cli.config_file = self.temp_config_file
        
        # Ensure clean slate by creating an empty config file
        with open(self.temp_config_file, 'w') as f:
            yaml.safe_dump([], f)
        
        # Reload config to ensure it's empty
        self.cli.endpoints = []

    def teardown_method(self):
        """Clean up the temporary config file after each test"""
        if os.path.exists(self.temp_config_file):
            os.remove(self.temp_config_file)
        self.cli.config_file = self.original_config_file

    def test_create_endpoint(self):
        """Test endpoint creation functionality"""
        # Create an endpoint
        self.cli.create_endpoint(
            hostname='localhost', 
            path='/api/test', 
            protocol='http', 
            port=8000, 
            data='{"status": "OK"}'
        )
        
        # Reload config to verify
        reloaded_endpoints = self.cli._load_config()
        
        assert len(reloaded_endpoints) == 1, f"Expected 1 endpoint, found {len(reloaded_endpoints)}"
        assert reloaded_endpoints[0]['hostname'] == 'localhost'
        assert reloaded_endpoints[0]['path'] == '/api/test'
        assert reloaded_endpoints[0]['protocol'] == 'http'
        assert reloaded_endpoints[0]['port'] == 8000
        assert reloaded_endpoints[0]['data'] == {"status": "OK"}

    def test_duplicate_endpoint(self):
        """Test prevention of duplicate endpoint creation"""
        # Create first endpoint
        self.cli.create_endpoint(
            hostname='localhost', 
            path='/api/test', 
            protocol='http', 
            port=8000
        )
        
        # Capture stdout to check print message
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Try to create the same endpoint again
        self.cli.create_endpoint(
            hostname='localhost', 
            path='/api/test', 
            protocol='http', 
            port=8000
        )
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Check that the output indicates duplicate endpoint
        assert "Endpoint already exists" in captured_output.getvalue()
        
        # Reload config to verify
        reloaded_endpoints = self.cli._load_config()
        
        assert len(reloaded_endpoints) == 1, f"Expected 1 endpoint, found {len(reloaded_endpoints)}"

    def test_uri_parsing(self):
        """Test URI parsing functionality"""
        # Test full URI parsing
        parsed_uri = self.cli.parse_uri(uri='http://example.com:8080/api/test')
        assert parsed_uri['protocol'] == 'http'
        assert parsed_uri['hostname'] == 'example.com'
        assert parsed_uri['path'] == '/api/test'
        assert parsed_uri['port'] == 8080
        
        # Test component-based parsing
        parsed_components = self.cli.parse_uri(
            hostname='localhost', 
            path='/api/status', 
            protocol='https', 
            port=443
        )
        assert parsed_components['protocol'] == 'https'
        assert parsed_components['hostname'] == 'localhost'
        assert parsed_components['path'] == '/api/status'
        assert parsed_components['port'] == 443
