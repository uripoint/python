"""
Tests for streaming protocol handlers
"""
import pytest
from uripoint.protocols import (
    RTSPHandler,
    HLSHandler,
    DASHHandler,
    get_protocol_handler
)

def test_rtsp_handler():
    """Test RTSP protocol handler"""
    handler = RTSPHandler()
    
    # Test valid configuration
    valid_config = {
        'stream_url': 'rtsp://camera.example.com/stream1',
        'transport': 'tcp',
        'auth': {
            'username': 'admin',
            'password': 'secure123'
        }
    }
    assert handler.validate_config(valid_config) is True
    
    # Test invalid transport
    invalid_transport = {
        'stream_url': 'rtsp://camera.example.com/stream1',
        'transport': 'invalid'
    }
    assert handler.validate_config(invalid_transport) is False
    
    # Test missing required fields
    missing_fields = {
        'transport': 'tcp'
    }
    assert handler.validate_config(missing_fields) is False
    
    # Test request handling
    endpoint_info = {'config': valid_config}
    response = handler.handle_request(endpoint_info)
    assert 'stream_url' in response
    assert 'transport' in response
    assert 'status' in response

def test_hls_handler():
    """Test HLS protocol handler"""
    handler = HLSHandler()
    
    # Test valid configuration
    valid_config = {
        'manifest_url': '/live/stream.m3u8',
        'segment_duration': 6,
        'playlist_size': 5,
        'options': {
            'bandwidth_variants': [
                {'resolution': '1080p', 'bitrate': 5000000},
                {'resolution': '720p', 'bitrate': 2500000}
            ]
        }
    }
    assert handler.validate_config(valid_config) is True
    
    # Test invalid segment duration
    invalid_duration = {
        'manifest_url': '/live/stream.m3u8',
        'segment_duration': 0
    }
    assert handler.validate_config(invalid_duration) is False
    
    # Test missing required fields
    missing_fields = {
        'manifest_url': '/live/stream.m3u8'
    }
    assert handler.validate_config(missing_fields) is False
    
    # Test request handling
    endpoint_info = {'config': valid_config}
    response = handler.handle_request(endpoint_info)
    assert 'manifest_url' in response
    assert 'segment_duration' in response
    assert 'status' in response

def test_dash_handler():
    """Test DASH protocol handler"""
    handler = DASHHandler()
    
    # Test valid configuration
    valid_config = {
        'mpd_url': '/vod/manifest.mpd',
        'segment_duration': 4,
        'options': {
            'quality_levels': [
                {'resolution': '2160p', 'bitrate': 15000000},
                {'resolution': '1080p', 'bitrate': 4500000}
            ]
        }
    }
    assert handler.validate_config(valid_config) is True
    
    # Test invalid segment duration
    invalid_duration = {
        'mpd_url': '/vod/manifest.mpd',
        'segment_duration': 0
    }
    assert handler.validate_config(invalid_duration) is False
    
    # Test missing required fields
    missing_fields = {
        'mpd_url': '/vod/manifest.mpd'
    }
    assert handler.validate_config(missing_fields) is False
    
    # Test request handling
    endpoint_info = {'config': valid_config}
    response = handler.handle_request(endpoint_info)
    assert 'mpd_url' in response
    assert 'segment_duration' in response
    assert 'status' in response

def test_protocol_factory():
    """Test protocol handler factory for streaming protocols"""
    # Test RTSP handler creation
    rtsp_handler = get_protocol_handler('rtsp')
    assert isinstance(rtsp_handler, RTSPHandler)
    
    # Test HLS handler creation
    hls_handler = get_protocol_handler('hls')
    assert isinstance(hls_handler, HLSHandler)
    
    # Test DASH handler creation
    dash_handler = get_protocol_handler('dash')
    assert isinstance(dash_handler, DASHHandler)
    
    # Test invalid protocol
    invalid_handler = get_protocol_handler('invalid')
    assert invalid_handler is None

def test_streaming_error_handling():
    """Test error handling in streaming protocols"""
    rtsp_handler = RTSPHandler()
    hls_handler = HLSHandler()
    dash_handler = DASHHandler()
    
    # Test RTSP with invalid endpoint info
    with pytest.raises(KeyError):
        rtsp_handler.handle_request({})
    
    # Test HLS with invalid endpoint info
    with pytest.raises(KeyError):
        hls_handler.handle_request({})
    
    # Test DASH with invalid endpoint info
    with pytest.raises(KeyError):
        dash_handler.handle_request({})

def test_streaming_connection():
    """Test connection handling in streaming protocols"""
    rtsp_handler = RTSPHandler()
    hls_handler = HLSHandler()
    dash_handler = DASHHandler()
    
    # Test connection methods
    assert rtsp_handler.connect() is True
    assert hls_handler.connect() is True
    assert dash_handler.connect() is True
