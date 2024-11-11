"""
UriPoint - A flexible Python library for managing network endpoints
"""

from .cli import UriPointCLI
from .router import StreamFilterRouter, get_url_parts, extract_query_params
from .protocols import (
    ProtocolHandler,
    MQTTHandler,
    RedisHandler,
    SMTPHandler,
    AMQPHandler,
    DNSHandler,
    get_protocol_handler,
    validate_endpoint_config,
    create_protocol_connection
)

__all__ = [
    'UriPointCLI',
    'StreamFilterRouter',
    'get_url_parts',
    'extract_query_params',
    'ProtocolHandler',
    'MQTTHandler',
    'RedisHandler',
    'SMTPHandler',
    'AMQPHandler',
    'DNSHandler',
    'get_protocol_handler',
    'validate_endpoint_config',
    'create_protocol_connection'
]
