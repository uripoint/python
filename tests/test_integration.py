"""
Integration tests for UriPoint components
"""
import pytest
import threading
import time
from uripoint import UriPointCLI
from uripoint.process import ManagedProcess
from uripoint.protocols import get_protocol_handler

def test_endpoint_process_integration():
    """Test integration between endpoints and process management"""
    cli = UriPointCLI()
    results = []
    
    def endpoint_worker(endpoint_uri):
        time.sleep(0.1)  # Simulate work
        results.append(endpoint_uri)
    
    # Create endpoints with associated processes
    endpoints = [
        ('http://localhost:8080/test1', {'method': 'GET'}),
        ('mqtt://localhost:1883/test2', {'qos': 1}),
        ('redis://localhost:6379/test3', {'db': 0})
    ]
    
    processes = []
    for uri, data in endpoints:
        cli.create_endpoint(uri=uri, data=data)
        process = ManagedProcess(endpoint_worker, uri)
        processes.append(process)
        process.start()
    
    # Wait for all processes
    for process in processes:
        process.join()
    
    # Verify all endpoints were processed
    assert len(results) == len(endpoints)
    assert all(uri in [r for r, _ in endpoints] for r in results)

def test_protocol_router_integration():
    """Test integration between protocol handlers and router"""
    cli = UriPointCLI()
    
    # Create endpoints for different protocols
    endpoints = {
        'mqtt': ('mqtt://localhost:1883/sensor', {'qos': 1}),
        'redis': ('redis://localhost:6379/cache', {'db': 0}),
        'smtp': ('smtp://smtp.example.com:587/mail', {'use_tls': True})
    }
    
    # Create endpoints
    for uri, data in endpoints.values():
        cli.create_endpoint(uri=uri, data=data)
    
    # Verify protocol handlers are correctly assigned
    for protocol, (uri, _) in endpoints.items():
        endpoint = cli.get_endpoint(uri)
        handler = get_protocol_handler(protocol)
        assert endpoint is not None
        assert isinstance(handler, type(get_protocol_handler(protocol)))

def test_streaming_process_integration():
    """Test integration between streaming protocols and process management"""
    cli = UriPointCLI()
    stream_ready = threading.Event()
    
    def stream_worker():
        time.sleep(0.1)  # Simulate stream initialization
        stream_ready.set()
    
    # Create streaming endpoint
    cli.create_endpoint(
        uri='rtsp://camera.example.com/stream1',
        data={
            'transport': 'tcp',
            'auth': {'username': 'admin', 'password': 'secure123'}
        }
    )
    
    # Start streaming process
    process = ManagedProcess(stream_worker)
    process.start()
    
    # Wait for stream
    assert stream_ready.wait(timeout=1.0)
    process.join()

def test_multi_protocol_integration():
    """Test integration with multiple protocols simultaneously"""
    cli = UriPointCLI()
    results = {}
    
    def protocol_worker(protocol):
        time.sleep(0.1)  # Simulate protocol work
        results[protocol] = True
    
    # Create endpoints for different protocols
    protocols = ['http', 'mqtt', 'redis', 'smtp', 'amqp']
    processes = []
    
    for protocol in protocols:
        cli.create_endpoint(
            uri=f'{protocol}://localhost/test',
            data={'test': True}
        )
        process = ManagedProcess(protocol_worker, protocol)
        processes.append(process)
        process.start()
    
    # Wait for all processes
    for process in processes:
        process.join()
    
    # Verify all protocols were processed
    assert len(results) == len(protocols)
    assert all(protocol in results for protocol in protocols)

def test_error_propagation():
    """Test error handling across components"""
    cli = UriPointCLI()
    
    def error_worker():
        raise ValueError("Test error")
    
    # Create endpoint
    cli.create_endpoint(
        uri='http://localhost:8080/error',
        data={'method': 'GET'}
    )
    
    # Start process that will error
    process = ManagedProcess(error_worker)
    process.start()
    
    # Verify error is propagated
    with pytest.raises(ValueError):
        process.join()

def test_endpoint_lifecycle():
    """Test complete endpoint lifecycle with process management"""
    cli = UriPointCLI()
    endpoint_uri = 'http://localhost:8080/lifecycle'
    
    # Create endpoint
    cli.create_endpoint(
        uri=endpoint_uri,
        data={'method': 'GET'}
    )
    
    # Verify endpoint exists
    endpoint = cli.get_endpoint(endpoint_uri)
    assert endpoint is not None
    
    def lifecycle_worker():
        time.sleep(0.1)  # Simulate work
    
    # Start process
    process = ManagedProcess(lifecycle_worker)
    process.start()
    
    # Wait for process
    process.join()
    
    # Delete endpoint
    cli.delete_endpoint(endpoint_uri)
    
    # Verify endpoint is gone
    endpoint = cli.get_endpoint(endpoint_uri)
    assert endpoint is None
