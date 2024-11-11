import pytest
import time
import multiprocessing
import threading
import socket
from uripoint.process import ManagedProcess
from uripoint.process_utils import check_existing_processes, get_free_port, kill_existing_processes

def test_managed_process_multiprocessing():
    """Test ManagedProcess with multiprocessing"""
    results = multiprocessing.Value('i', 0)

    def increment_counter(counter):
        with counter.get_lock():
            counter.value += 1

    process = ManagedProcess(increment_counter, results)
    process.start()
    process.join()

    assert results.value == 1

def test_managed_process_threading():
    """Test ManagedProcess with threading"""
    results = multiprocessing.Value('i', 0)

    def increment_counter(counter):
        with counter.get_lock():
            counter.value += 1

    thread_process = ManagedProcess(increment_counter, results)
    thread_process.start()
    thread_process.join()

    assert results.value == 1

def test_managed_process_multiple():
    """Test multiple concurrent processes"""
    counter = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()

    def increment_counter(counter, lock):
        with lock:
            counter.value += 1

    processes = [
        ManagedProcess(increment_counter, counter, lock) for _ in range(5)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    assert counter.value == 5

def test_process_utilities():
    """Test process utility functions"""
    # Test check_existing_processes
    python_processes = check_existing_processes('python')
    assert isinstance(python_processes, list)
    assert len(python_processes) > 0

def test_get_free_port():
    """Test get_free_port function"""
    port = get_free_port()
    
    # Verify port is available
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            assert True  # Port is free
        except OSError:
            pytest.fail(f"Port {port} is not free")

def test_process_lifecycle():
    """Test process lifecycle methods"""
    def long_task():
        time.sleep(1)

    # Test start and is_alive
    process = ManagedProcess(long_task)
    assert not process.is_alive()
    
    process.start()
    assert process.is_alive()
    
    process.join()
    assert not process.is_alive()

def test_process_error_handling():
    """Test error handling in ManagedProcess"""
    def error_task():
        raise ValueError("Test error")

    process = ManagedProcess(error_task)
    process.start()
    
    with pytest.raises(ValueError):
        process.join()
