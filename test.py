import pytest
from uripoint.main import UriPointCLI
import os
import tempfile
import yaml

def test_uripoint_cli_create_endpoint():
    """Test endpoint creation functionality"""
    cli = UriPointCLI()
    
    # Use a temporary config file for testing
    original_config_file = cli.config_file
    cli.config_file = os.path.join(tempfile.gettempdir(), 'test_uripoint_config.yaml')
    
    try:
        # Create an endpoint
        cli.create_endpoint(
            hostname='localhost', 
            path='/api/test', 
            protocol='http', 
            port=8000, 
            data='{"status": "OK"}'
        )
        
        # Load the config and verify
        with open(cli.config_file, 'r') as f:
            endpoints = yaml.safe_load(f)
        
        assert len(endpoints) == 1
        assert endpoints[0]['hostname'] == 'localhost'
        assert endpoints[0]['path'] == '/api/test'
        assert endpoints[0]['protocol'] == 'http'
        assert endpoints[0]['port'] == 8000
        assert endpoints[0]['data'] == {"status": "OK"}
    
    finally:
        # Clean up test config file
        if os.path.exists(cli.config_file):
            os.remove(cli.config_file)
        
        # Restore original config file path
        cli.config_file = original_config_file

def test_uripoint_cli_duplicate_endpoint():
    """Test prevention of duplicate endpoint creation"""
    cli = UriPointCLI()
    
    # Use a temporary config file for testing
    original_config_file = cli.config_file
    cli.config_file = os.path.join(tempfile.gettempdir(), 'test_uripoint_duplicate_config.yaml')
    
    try:
        # Create first endpoint
        cli.create_endpoint(
            hostname='localhost', 
            path='/api/test', 
            protocol='http', 
            port=8000
        )
        
        # Try to create the same endpoint again
        import io
        import sys
        
        # Capture stdout to check print message
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        cli.create_endpoint(
            hostname='localhost', 
            path='/api/test', 
            protocol='http', 
            port=8000
        )
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Check that the output indicates duplicate endpoint
        assert "Endpoint already exists" in captured_output.getvalue()
        
        # Load the config and verify only one endpoint exists
        with open(cli.config_file, 'r') as f:
            endpoints = yaml.safe_load(f)
        
        assert len(endpoints) == 1
    
    finally:
        # Clean up test config file
        if os.path.exists(cli.config_file):
            os.remove(cli.config_file)
        
        # Restore original config file path
        cli.config_file = original_config_file

def test_uripoint_uri_parsing():
    """Test URI parsing functionality"""
    cli = UriPointCLI()
    
    # Test full URI parsing
    parsed_uri = cli.parse_uri(uri='http://example.com:8080/api/test')
    assert parsed_uri['protocol'] == 'http'
    assert parsed_uri['hostname'] == 'example.com'
    assert parsed_uri['path'] == '/api/test'
    assert parsed_uri['port'] == 8080
    
    # Test component-based parsing
    parsed_components = cli.parse_uri(
        hostname='localhost', 
        path='/api/status', 
        protocol='https', 
        port=443
    )
    assert parsed_components['protocol'] == 'https'
    assert parsed_components['hostname'] == 'localhost'
    assert parsed_components['path'] == '/api/status'
    assert parsed_components['port'] == 443
