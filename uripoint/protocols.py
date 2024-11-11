"""
Protocol handlers for UriPoint
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import json

class ProtocolHandler(ABC):
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    def handle_request(self, endpoint_info: Dict[str, Any], method: str = 'GET') -> str:
        """Handle incoming request for the endpoint"""
        return json.dumps(endpoint_info.get('config', {}).get('response', {}))

class HTTPHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        # HTTP endpoints require a response configuration and method
        if 'response' not in config:
            return False
        
        # Validate methods if specified
        if 'methods' in config:
            valid_methods = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}
            methods = set(method.upper() for method in config['methods'])
            if not methods.issubset(valid_methods):
                return False
        
        return True

    def connect(self) -> bool:
        return True

class RTSPHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['stream_url', 'transport']
        if not all(field in config for field in required_fields):
            return False
        
        valid_transports = {'udp', 'tcp', 'http'}
        return config['transport'].lower() in valid_transports

    def connect(self) -> bool:
        return True

    def handle_request(self, endpoint_info: Dict[str, Any], method: str = 'GET') -> str:
        config = endpoint_info.get('config', {})
        return json.dumps({
            'stream_url': config.get('stream_url'),
            'transport': config.get('transport'),
            'status': 'streaming'
        })

class HLSHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['manifest_url', 'segment_duration']
        if not all(field in config for field in required_fields):
            return False
        
        # Validate segment duration (typically 2-10 seconds)
        return 1 <= config['segment_duration'] <= 10

    def connect(self) -> bool:
        return True

    def handle_request(self, endpoint_info: Dict[str, Any], method: str = 'GET') -> str:
        config = endpoint_info.get('config', {})
        return json.dumps({
            'manifest_url': config.get('manifest_url'),
            'segment_duration': config.get('segment_duration'),
            'status': 'streaming'
        })

class DASHHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['mpd_url', 'segment_duration']
        if not all(field in config for field in required_fields):
            return False
        
        # Validate segment duration
        return 1 <= config['segment_duration'] <= 10

    def connect(self) -> bool:
        return True

    def handle_request(self, endpoint_info: Dict[str, Any], method: str = 'GET') -> str:
        config = endpoint_info.get('config', {})
        return json.dumps({
            'mpd_url': config.get('mpd_url'),
            'segment_duration': config.get('segment_duration'),
            'status': 'streaming'
        })

class MQTTHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['topic', 'qos']
        if not all(field in config for field in required_fields):
            return False
        
        # Validate QoS level (0, 1, or 2)
        return config['qos'] in [0, 1, 2]

    def connect(self) -> bool:
        return True

    def handle_request(self, endpoint_info: Dict[str, Any], method: str = 'GET') -> str:
        config = endpoint_info.get('config', {})
        return json.dumps({
            'topic': config.get('topic'),
            'qos': config.get('qos'),
            'status': 'connected'
        })

class WebSocketHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['protocol']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        return True

class RedisHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        optional_fields = ['db', 'decode_responses', 'max_connections']
        return isinstance(config, dict)

    def connect(self) -> bool:
        return True

class SMTPHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['use_tls']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        return True

class AMQPHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['exchange']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        return True

class DNSHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['timeout']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        return True

def get_protocol_handler(protocol: str) -> Optional[ProtocolHandler]:
    """
    Factory function to get the appropriate protocol handler
    """
    handlers = {
        'http': HTTPHandler,
        'https': HTTPHandler,
        'rtsp': RTSPHandler,
        'hls': HLSHandler,
        'dash': DASHHandler,
        'mqtt': MQTTHandler,
        'ws': WebSocketHandler,
        'wss': WebSocketHandler,
        'redis': RedisHandler,
        'smtp': SMTPHandler,
        'amqp': AMQPHandler,
        'dns': DNSHandler
    }
    
    handler_class = handlers.get(protocol)
    if handler_class:
        return handler_class()
    return None

def validate_endpoint_config(protocol: str, config: Dict[str, Any]) -> bool:
    """
    Validate endpoint configuration for a specific protocol
    """
    handler = get_protocol_handler(protocol)
    if handler:
        return handler.validate_config(config)
    return False

def create_protocol_connection(protocol: str) -> bool:
    """
    Create a connection for a specific protocol
    """
    handler = get_protocol_handler(protocol)
    if handler:
        return handler.connect()
    return False
