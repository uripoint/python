import psutil
import os
import signal

def check_existing_processes(process_name):
    """
    Check for existing processes with a given name
    
    :param process_name: Name of the process to check
    :return: List of existing process PIDs
    """
    existing_processes = []
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == process_name:
                existing_processes.append(proc.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return existing_processes

def kill_existing_processes(process_name):
    """
    Kill existing processes with a given name
    
    :param process_name: Name of the process to kill
    """
    for pid in check_existing_processes(process_name):
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

def get_free_port(start_port=8000, end_port=65535):
    """
    Find a free port in the given range
    
    :param start_port: Starting port to check
    :param end_port: Ending port to check
    :return: First available free port
    """
    import socket
    
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    
    raise RuntimeError(f"No free port found between {start_port} and {end_port}")
