"""
CLI interface for UriPoint
"""
from typing import Dict, Any, List, Optional
from .router import StreamFilterRouter, get_url_parts

class UriPointCLI:
    def __init__(self):
        self.router = StreamFilterRouter()
    
    def create_endpoint(self, uri: str, data: Dict[str, Any]) -> bool:
        """
        Create a new endpoint
        
        :param uri: URI for the endpoint
        :param data: Configuration data for the endpoint
        :return: Success status
        """
        try:
            return self.router.add_endpoint(uri, data)
        except ValueError as e:
            raise ValueError(f"Failed to create endpoint: {str(e)}")
    
    def list_endpoints(self) -> List[Dict[str, Any]]:
        """
        List all registered endpoints
        
        :return: List of endpoint configurations
        """
        endpoints = self.router.get_endpoints()
        return [
            {
                'protocol': info['protocol'],
                'hostname': info['hostname'],
                'port': info['port'],
                'path': info['path']
            }
            for info in endpoints.values()
        ]
    
    def get_endpoint(self, uri: str) -> Optional[Dict[str, Any]]:
        """
        Get endpoint configuration by URI
        
        :param uri: URI of the endpoint
        :return: Endpoint configuration if found
        """
        endpoints = self.router.get_endpoints()
        return endpoints.get(uri)
    
    def publish(self, uri: str, data: Any) -> bool:
        """
        Publish data to an endpoint
        
        :param uri: URI of the endpoint
        :param data: Data to publish
        :return: Success status
        """
        return bool(self.router.process(uri, data))
    
    def subscribe(self, uri: str, callback: callable) -> bool:
        """
        Subscribe to an endpoint
        
        :param uri: URI of the endpoint
        :param callback: Callback function for received data
        :return: Success status
        """
        pattern = get_url_parts(uri)['path']
        self.router.add_route(pattern, callback)
        return True
    
    def serve(self) -> None:
        """
        Start serving all endpoints
        """
        # Implementation for serving endpoints
        pass
