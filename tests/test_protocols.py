"""
Tests for protocol implementations
"""
import pytest
from uripoint import UriPointCLI

def test_mqtt_endpoint():
    cli = UriPointCLI()
    
    # Test MQTT endpoint creation
    cli.create_endpoint(
        uri='mqtt://localhost:1883/test/topic',
        data={'qos': 1, 'retain': True}
    )
    
    endpoints = cli.list_endpoints()
    mqtt_endpoint = next((e for e in endpoints if e['protocol'] == 'mqtt'), None)
    
    assert mqtt_endpoint is not None
    assert mqtt_endpoint['hostname'] == 'localhost'
    assert mqtt_endpoint['port'] == 1883
    assert mqtt_endpoint['path'] == '/test/topic'

def test_redis_endpoint():
    cli = UriPointCLI()
    
    # Test Redis endpoint creation
    cli.create_endpoint(
        uri='redis://localhost:6379/0',
        data={'decode_responses': True}
    )
    
    endpoints = cli.list_endpoints()
    redis_endpoint = next((e for e in endpoints if e['protocol'] == 'redis'), None)
    
    assert redis_endpoint is not None
    assert redis_endpoint['hostname'] == 'localhost'
    assert redis_endpoint['port'] == 6379
    assert redis_endpoint['path'] == '/0'

def test_smtp_endpoint():
    cli = UriPointCLI()
    
    # Test SMTP endpoint creation
    cli.create_endpoint(
        uri='smtp://smtp.example.com:587/mail',
        data={'use_tls': True}
    )
    
    endpoints = cli.list_endpoints()
    smtp_endpoint = next((e for e in endpoints if e['protocol'] == 'smtp'), None)
    
    assert smtp_endpoint is not None
    assert smtp_endpoint['hostname'] == 'smtp.example.com'
    assert smtp_endpoint['port'] == 587
    assert smtp_endpoint['path'] == '/mail'

def test_amqp_endpoint():
    cli = UriPointCLI()
    
    # Test AMQP endpoint creation
    cli.create_endpoint(
        uri='amqp://localhost:5672/queue',
        data={'exchange': 'test_exchange', 'durable': True}
    )
    
    endpoints = cli.list_endpoints()
    amqp_endpoint = next((e for e in endpoints if e['protocol'] == 'amqp'), None)
    
    assert amqp_endpoint is not None
    assert amqp_endpoint['hostname'] == 'localhost'
    assert amqp_endpoint['port'] == 5672
    assert amqp_endpoint['path'] == '/queue'

def test_dns_endpoint():
    cli = UriPointCLI()
    
    # Test DNS endpoint creation
    cli.create_endpoint(
        uri='dns://8.8.8.8:53/lookup',
        data={'timeout': 5, 'cache_enabled': True}
    )
    
    endpoints = cli.list_endpoints()
    dns_endpoint = next((e for e in endpoints if e['protocol'] == 'dns'), None)
    
    assert dns_endpoint is not None
    assert dns_endpoint['hostname'] == '8.8.8.8'
    assert dns_endpoint['port'] == 53
    assert dns_endpoint['path'] == '/lookup'

def test_endpoint_validation():
    cli = UriPointCLI()
    
    # Test invalid protocol
    with pytest.raises(ValueError):
        cli.create_endpoint(
            uri='invalid://localhost:1234/test',
            data={}
        )
    
    # Test invalid port
    with pytest.raises(ValueError):
        cli.create_endpoint(
            uri='mqtt://localhost:99999/test',
            data={}
        )
    
    # Test missing required data
    with pytest.raises(ValueError):
        cli.create_endpoint(
            uri='smtp://smtp.example.com:587/mail',
            data={}  # Missing required TLS setting
        )
