#!/usr/bin/env python3
"""
Example usage of UriPoint ManagedProcess and process utilities
"""

import time
from uripoint.process import ManagedProcess
from uripoint.process_utils import check_existing_processes, get_free_port, kill_existing_processes

def long_running_task(name, duration=5):
    """
    Simulate a long-running task
    
    :param name: Name of the task
    :param duration: Duration of the task in seconds
    """
    print(f"Starting task: {name}")
    for i in range(duration):
        print(f"{name}: Running - {i+1}/{duration} seconds")
        time.sleep(1)
    print(f"Task {name} completed")

def main():
    # Demonstrate process management
    print("Process Management Example")
    
    # Create managed processes
    task1 = ManagedProcess(target=long_running_task, args=('Task A', 3))
    task2 = ManagedProcess(target=long_running_task, args=('Task B', 5))
    
    # Start processes
    print("\nStarting processes:")
    process1 = task1.start()
    process2 = task2.start()
    
    # Check if processes are alive
    print("\nChecking process status:")
    print(f"Task A running: {task1.is_alive()}")
    print(f"Task B running: {task2.is_alive()}")
    
    # Wait for processes to complete
    task1.join()
    task2.join()
    
    # Process utilities demonstration
    print("\nProcess Utilities:")
    
    # Find existing processes
    python_processes = check_existing_processes('python')
    print(f"Existing Python processes: {len(python_processes)}")
    
    # Find a free port
    free_port = get_free_port()
    print(f"Found free port: {free_port}")
    
    # Demonstrate killing processes (commented out for safety)
    # kill_existing_processes('python')

if __name__ == '__main__':
    main()
