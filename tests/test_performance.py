"""
Performance and stress testing for UriPoint
"""
import time
import pytest
import concurrent.futures
from uripoint import UriPointCLI

def test_endpoint_creation_performance():
    """Test performance of endpoint creation"""
    cli = UriPointCLI()
    start_time = time.time()
    iterations = 100
    
    for i in range(iterations):
        cli.create_endpoint(
            uri=f'http://localhost:808{i%10}/test{i}',
            data={'method': 'GET'}
        )
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Assert creation time is reasonable (less than 5ms per endpoint)
    assert duration/iterations < 0.005

def test_concurrent_endpoint_access():
    """Test concurrent access to endpoints"""
    cli = UriPointCLI()
    num_concurrent = 50
    
    # Create test endpoint
    cli.create_endpoint(
        uri='http://localhost:8080/test',
        data={'method': 'GET'}
    )
    
    def access_endpoint():
        return cli.get_endpoint('http://localhost:8080/test')
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = [executor.submit(access_endpoint) for _ in range(num_concurrent)]
        results = [f.result() for f in futures]
    
    assert len(results) == num_concurrent
    assert all(r is not None for r in results)

def test_endpoint_stress():
    """Stress test endpoint management"""
    cli = UriPointCLI()
    iterations = 1000
    
    for i in range(iterations):
        # Create endpoint
        cli.create_endpoint(
            uri=f'http://localhost:8080/stress{i}',
            data={'method': 'GET'}
        )
        
        # List endpoints
        endpoints = cli.list_endpoints()
        assert len(endpoints) > i
        
        # Get specific endpoint
        endpoint = cli.get_endpoint(f'http://localhost:8080/stress{i}')
        assert endpoint is not None
        
        # Delete if i is even
        if i % 2 == 0:
            cli.delete_endpoint(f'http://localhost:8080/stress{i}')
            endpoint = cli.get_endpoint(f'http://localhost:8080/stress{i}')
            assert endpoint is None

def test_protocol_handler_performance():
    """Test performance of protocol handlers"""
    cli = UriPointCLI()
    protocols = ['http', 'mqtt', 'redis', 'smtp', 'amqp']
    iterations = 20
    
    start_time = time.time()
    
    for protocol in protocols:
        for i in range(iterations):
            cli.create_endpoint(
                uri=f'{protocol}://localhost/test{i}',
                data={'test': True}
            )
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Assert handler creation time is reasonable
    assert duration/(len(protocols) * iterations) < 0.01

def test_memory_usage():
    """Test memory usage under load"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    cli = UriPointCLI()
    large_iterations = 10000
    
    # Create many endpoints
    for i in range(large_iterations):
        cli.create_endpoint(
            uri=f'http://localhost:8080/memory{i}',
            data={'method': 'GET'}
        )
    
    final_memory = process.memory_info().rss
    memory_per_endpoint = (final_memory - initial_memory) / large_iterations
    
    # Assert reasonable memory usage (less than 1KB per endpoint)
    assert memory_per_endpoint < 1024

def test_error_handling_under_load():
    """Test error handling under heavy load"""
    cli = UriPointCLI()
    iterations = 1000
    
    for i in range(iterations):
        # Mix of valid and invalid operations
        if i % 3 == 0:
            # Invalid protocol
            with pytest.raises(ValueError):
                cli.create_endpoint(
                    uri=f'invalid://localhost/test{i}',
                    data={}
                )
        elif i % 3 == 1:
            # Invalid port
            with pytest.raises(ValueError):
                cli.create_endpoint(
                    uri=f'http://localhost:99999/test{i}',
                    data={}
                )
        else:
            # Valid endpoint
            cli.create_endpoint(
                uri=f'http://localhost:8080/test{i}',
                data={'method': 'GET'}
            )
