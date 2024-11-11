import multiprocessing
import threading
import time

class ManagedProcess:
    def __init__(self, target=None, args=(), kwargs=None):
        """
        A wrapper for managing processes and threads
        
        :param target: Function to be executed
        :param args: Positional arguments for the target function
        :param kwargs: Keyword arguments for the target function
        """
        self.kwargs = kwargs or {}
        self.args = args
        self.target = target
        self._process = None
        self._thread = None

    def start(self):
        """
        Start the process or thread based on the target
        
        :return: Process or thread instance
        """
        if self.target is None:
            raise ValueError("No target function provided")
        
        # Determine whether to use multiprocessing or threading
        if hasattr(self.target, '__call__'):
            try:
                self._process = multiprocessing.Process(
                    target=self.target, 
                    args=self.args, 
                    kwargs=self.kwargs
                )
                self._process.start()
                return self._process
            except Exception:
                self._thread = threading.Thread(
                    target=self.target, 
                    args=self.args, 
                    kwargs=self.kwargs
                )
                self._thread.start()
                return self._thread
        
        raise TypeError("Target must be a callable")

    def join(self, timeout=None):
        """
        Wait for the process or thread to complete
        
        :param timeout: Maximum wait time
        """
        if self._process:
            self._process.join(timeout)
        elif self._thread:
            self._thread.join(timeout)

    def is_alive(self):
        """
        Check if the process or thread is still running
        
        :return: Boolean indicating if process/thread is alive
        """
        if self._process:
            return self._process.is_alive()
        elif self._thread:
            return self._thread.is_alive()
        return False

    def terminate(self):
        """
        Terminate the process if it's a multiprocessing process
        """
        if self._process and hasattr(self._process, 'terminate'):
            self._process.terminate()
