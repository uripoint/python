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
        # HTTP doesn't require persistent connection
        return True

    def handle_request(self, endpoint_info: Dict[str, Any], method: str = 'GET') -> str:
        """
        Handle HTTP request based on method
        
        :param endpoint_info: Endpoint configuration
        :param method: HTTP method used
        :return: JSON response
        """
        config = endpoint_info.get('config', {})
        allowed_methods = {m.upper() for m in config.get('methods', ['GET'])}
        
        if method.upper() not in allowed_methods:
            raise ValueError(f"Method {method} not allowed. Allowed methods: {allowed_methods}")
        
        response_data = config.get('response', {})
        if isinstance(response_data, dict):
            response_data['allowed_methods'] = list(allowed_methods)
        
        return json.dumps(response_data)

class MQTTHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['qos']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        # Implementation for MQTT connection
        return True

class RedisHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        # Redis has no required fields, but validate optional ones
        optional_fields = ['db', 'decode_responses', 'max_connections']
        return isinstance(config, dict)

    def connect(self) -> bool:
        # Implementation for Redis connection
        return True

class SMTPHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['use_tls']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        # Implementation for SMTP connection
        return True

class AMQPHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['exchange']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        # Implementation for AMQP connection
        return True

class DNSHandler(ProtocolHandler):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ['timeout']
        return all(field in config for field in required_fields)

    def connect(self) -> bool:
        # Implementation for DNS connection
        return True

def get_protocol_handler(protocol: str) -> Optional[ProtocolHandler]:
    """
    Factory function to get the appropriate protocol handler
    """
    handlers = {
        'http': HTTPHandler,
        'https': HTTPHandler,
        'mqtt': MQTTHandler,
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
