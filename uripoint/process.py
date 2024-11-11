"""
Process management utilities for UriPoint
"""
import threading
import multiprocessing
from typing import Any, Callable, Optional, Dict, Tuple

class ManagedProcess:
    """
    A managed process class that handles process lifecycle and error propagation
    """
    def __init__(self, target: Callable, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.error_queue = multiprocessing.Queue()
        self._process = None
        
    def _wrapped_target(self):
        """
        Wrapper for the target function that captures errors
        """
        try:
            result = self.target(*self.args, **self.kwargs)
            self.error_queue.put(None)  # No error
            return result
        except Exception as e:
            self.error_queue.put(e)
            raise  # Re-raise to ensure process terminates with error
            
    def start(self):
        """
        Start the managed process
        """
        if self._process is None:
            self._process = multiprocessing.Process(
                target=self._wrapped_target
            )
            self._process.start()
            
    def join(self, timeout: Optional[float] = None):
        """
        Join the process and check for errors
        
        :param timeout: Optional timeout in seconds
        """
        if self._process:
            self._process.join(timeout)
            
            # Check for errors
            try:
                error = self.error_queue.get(block=False)
                if error:
                    raise error
            except multiprocessing.queues.Empty:
                # No error occurred or process hasn't finished
                pass
                
    def terminate(self):
        """
        Terminate the process
        """
        if self._process:
            self._process.terminate()
            self._process.join()
            
    def is_alive(self) -> bool:
        """
        Check if the process is alive
        
        :return: Process alive status
        """
        return bool(self._process and self._process.is_alive())

class ProcessManager:
    """
    Manager for handling multiple processes
    """
    def __init__(self):
        self.processes: Dict[str, ManagedProcess] = {}
        self._lock = threading.Lock()
        
    def start_process(self, name: str, target: Callable, *args, **kwargs) -> bool:
        """
        Start a new managed process
        
        :param name: Process name
        :param target: Target function
        :return: Success status
        """
        with self._lock:
            if name in self.processes:
                return False
                
            process = ManagedProcess(target, *args, **kwargs)
            self.processes[name] = process
            process.start()
            return True
            
    def stop_process(self, name: str) -> bool:
        """
        Stop a managed process
        
        :param name: Process name
        :return: Success status
        """
        with self._lock:
            process = self.processes.get(name)
            if process:
                process.terminate()
                del self.processes[name]
                return True
            return False
            
    def get_process(self, name: str) -> Optional[ManagedProcess]:
        """
        Get a process by name
        
        :param name: Process name
        :return: ManagedProcess instance if found
        """
        return self.processes.get(name)
        
    def list_processes(self) -> Dict[str, bool]:
        """
        List all processes and their status
        
        :return: Dictionary of process names and alive status
        """
        return {name: proc.is_alive() for name, proc in self.processes.items()}
        
    def cleanup(self):
        """
        Clean up all processes
        """
        with self._lock:
            for process in self.processes.values():
                process.terminate()
            self.processes.clear()
