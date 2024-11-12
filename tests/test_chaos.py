"""
Chaos testing for UriPoint
Tests system resilience under unpredictable conditions
"""
import pytest
import random
import threading
import time
import signal
import os
from uripoint import UriPointCLI
from uripoint.process import ManagedProcess

class ChaosThread(threading.Thread):
    def __init__(self, target, *args, **kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._stop_event = threading.Event()
    
    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.is_set()

def test_random_endpoint_chaos():
    """Test system stability with random endpoint creation/deletion"""
    cli = UriPointCLI()
    chaos_duration = 2  # seconds
    
    def chaos_worker():
        start_time = time.time()
        while time.time() - start_time < chaos_duration:
            try:
                # Random operations
                op = random.choice(['create', 'delete', 'get', 'list'])
                
                if op == 'create':
                    protocol = random.choice(['http', 'mqtt', 'redis', 'smtp', 'amqp'])
                    port = random.randint(1024, 65535)
                    cli.create_endpoint(
                        uri=f'{protocol}://localhost:{port}/chaos',
                        data={'test': True}
                    )
                elif op == 'delete':
                    endpoints = cli.list_endpoints()
                    if endpoints:
                        endpoint = random.choice(endpoints)
                        cli.delete_endpoint(endpoint['uri'])
                elif op == 'get':
                    endpoints = cli.list_endpoints()
                    if endpoints:
                        endpoint = random.choice(endpoints)
                        cli.get_endpoint(endpoint['uri'])
                else:  # list
                    cli.list_endpoints()
                
                # Random sleep
                time.sleep(random.uniform(0, 0.1))
            except Exception:
                # Expect and ignore some errors during chaos
                pass
    
    # Start chaos threads
    threads = [ChaosThread(target=chaos_worker) for _ in range(5)]
    for thread in threads:
        thread.start()
    
    # Let chaos run
    time.sleep(chaos_duration)
    
    # Stop chaos
    for thread in threads:
        thread.stop()
        thread.join()
    
    # Verify system is still operational
    try:
        cli.create_endpoint(
            uri='http://localhost:8080/test',
            data={'method': 'GET'}
        )
        endpoints = cli.list_endpoints()
        assert any(e['uri'] == 'http://localhost:8080/test' for e in endpoints)
    except Exception as e:
        pytest.fail(f"System not operational after chaos: {str(e)}")

def test_process_chaos():
    """Test system stability with chaotic process management"""
    cli = UriPointCLI()
    processes = []
    chaos_duration = 2  # seconds
    
    def normal_worker():
        while True:
            time.sleep(0.1)
    
    def chaos_worker():
        start_time = time.time()
        while time.time() - start_time < chaos_duration:
            try:
                # Random process operations
                op = random.choice(['create', 'terminate'])
                
                if op == 'create':
                    process = ManagedProcess(normal_worker)
                    process.start()
                    processes.append(process)
                elif op == 'terminate' and processes:
                    process = random.choice(processes)
                    try:
                        os.kill(process.pid, signal.SIGTERM)
                    except:
                        pass  # Process might already be terminated
                
                time.sleep(random.uniform(0, 0.1))
            except Exception:
                # Expect and ignore some errors during chaos
                pass
    
    # Start chaos threads
    threads = [ChaosThread(target=chaos_worker) for _ in range(3)]
    for thread in threads:
        thread.start()
    
    # Let chaos run
    time.sleep(chaos_duration)
    
    # Stop chaos
    for thread in threads:
        thread.stop()
        thread.join()
    
    # Clean up any remaining processes
    for process in processes:
        try:
            process.terminate()
            process.join()
        except:
            pass

def test_network_chaos():
    """Test system stability with network chaos"""
    cli = UriPointCLI()
    chaos_duration = 2  # seconds
    
    def network_chaos_worker():
        start_time = time.time()
        while time.time() - start_time < chaos_duration:
            try:
                # Simulate network issues with invalid endpoints
                protocol = random.choice(['http', 'mqtt', 'redis', 'smtp', 'amqp'])
                port = random.randint(1, 65535)
                invalid_host = f'invalid{random.randint(1,1000)}.local'
                
                cli.create_endpoint(
                    uri=f'{protocol}://{invalid_host}:{port}/chaos',
                    data={'test': True}
                )
                
                time.sleep(random.uniform(0, 0.1))
            except Exception:
                # Expect and ignore network errors
                pass
    
    # Start chaos threads
    threads = [ChaosThread(target=network_chaos_worker) for _ in range(3)]
    for thread in threads:
        thread.start()
    
    # Let chaos run
    time.sleep(chaos_duration)
    
    # Stop chaos
    for thread in threads:
        thread.stop()
        thread.join()
    
    # Verify system can still handle valid endpoints
    try:
        cli.create_endpoint(
            uri='http://localhost:8080/test',
            data={'method': 'GET'}
        )
        assert cli.get_endpoint('http://localhost:8080/test') is not None
    except Exception as e:
        pytest.fail(f"System not operational after network chaos: {str(e)}")

def test_data_chaos():
    """Test system stability with chaotic data inputs"""
    cli = UriPointCLI()
    chaos_duration = 2  # seconds
    
    def data_chaos_worker():
        start_time = time.time()
        while time.time() - start_time < chaos_duration:
            try:
                # Generate random malformed data
                data = {
                    'test': random.choice([None, '', {}, [], set()]),
                    'number': random.choice([float('inf'), float('nan'), -1]),
                    'string': ''.join(chr(random.randint(0, 255)) for _ in range(10)),
                    'nested': {'deep': {'deeper': random.randint(-1000, 1000)}}
                }
                
                protocol = random.choice(['http', 'mqtt', 'redis', 'smtp', 'amqp'])
                cli.create_endpoint(
                    uri=f'{protocol}://localhost:8080/chaos',
                    data=data
                )
                
                time.sleep(random.uniform(0, 0.1))
            except Exception:
                # Expect and ignore data validation errors
                pass
    
    # Start chaos threads
    threads = [ChaosThread(target=data_chaos_worker) for _ in range(3)]
    for thread in threads:
        thread.start()
    
    # Let chaos run
    time.sleep(chaos_duration)
    
    # Stop chaos
    for thread in threads:
        thread.stop()
        thread.join()
    
    # Verify system can still handle valid data
    try:
        cli.create_endpoint(
            uri='http://localhost:8080/test',
            data={'method': 'GET'}
        )
        assert cli.get_endpoint('http://localhost:8080/test') is not None
    except Exception as e:
        pytest.fail(f"System not operational after data chaos: {str(e)}")
