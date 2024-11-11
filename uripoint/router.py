import re
from typing import Dict, Any, Callable, Optional
from .protocols import validate_endpoint_config, create_protocol_connection

class StreamFilterRouter:
    """
    A flexible router for handling and filtering stream-based communications
    """
    def __init__(self):
        self.routes = {}
        self.filters = {}
        self.endpoints = {}

    def add_route(self, pattern: str, handler: Callable):
        """
        Add a route with a pattern and corresponding handler
        
        :param pattern: Regex pattern to match
        :param handler: Function to handle matched routes
        """
        self.routes[pattern] = handler

    def add_filter(self, name: str, filter_func: Callable):
        """
        Add a filter for stream processing
        
        :param name: Name of the filter
        :param filter_func: Function to apply filtering
        """
        self.filters[name] = filter_func

    def add_endpoint(self, uri: str, config: Dict[str, Any]) -> bool:
        """
        Add an endpoint with configuration
        
        :param uri: URI of the endpoint
        :param config: Configuration for the endpoint
        :return: Success status
        """
        parts = get_url_parts(uri)
        protocol = parts['scheme']
        
        if not validate_endpoint_config(protocol, config):
            raise ValueError(f"Invalid configuration for protocol {protocol}")
        
        endpoint_id = uri
        self.endpoints[endpoint_id] = {
            'uri': uri,
            'protocol': protocol,
            'hostname': parts['netloc'].split(':')[0],
            'port': int(parts['netloc'].split(':')[1]) if ':' in parts['netloc'] else None,
            'path': parts['path'],
            'config': config
        }
        
        return create_protocol_connection(protocol)

    def match_route(self, uri: str) -> Optional[Callable]:
        """
        Match a URI to a registered route
        
        :param uri: URI to match
        :return: Matched handler or None
        """
        for pattern, handler in self.routes.items():
            if re.match(pattern, uri):
                return handler
        return None

    def apply_filters(self, data: Any) -> Any:
        """
        Apply registered filters to input data
        
        :param data: Input data to filter
        :return: Filtered data
        """
        result = data
        for filter_name, filter_func in self.filters.items():
            result = filter_func(result)
        return result

    def process(self, uri: str, data: Any) -> Any:
        """
        Process a URI with matching route and filters
        
        :param uri: URI to process
        :param data: Data to process
        :return: Processed result
        """
        handler = self.match_route(uri)
        if handler:
            filtered_data = self.apply_filters(data)
            return handler(filtered_data)
        return None

    def get_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered endpoints
        
        :return: Dictionary of endpoints
        """
        return self.endpoints

def get_url_parts(url: str) -> Dict[str, str]:
    """
    Extract parts of a URL
    
    :param url: URL to parse
    :return: Dictionary of URL components
    """
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(url)
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'path': parsed.path,
        'params': parsed.params,
        'query': parse_qs(parsed.query),
        'fragment': parsed.fragment
    }

def extract_query_params(url: str) -> Dict[str, str]:
    """
    Extract query parameters from a URL
    
    :param url: URL to extract parameters from
    :return: Dictionary of query parameters
    """
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(url)
    return parse_qs(parsed.query)

def convert_file_path(path: str, base_dir: Optional[str] = None) -> str:
    """
    Convert and normalize file paths
    
    :param path: Input file path
    :param base_dir: Optional base directory
    :return: Normalized file path
    """
    import os

    if base_dir:
        path = os.path.join(base_dir, path)
    
    return os.path.normpath(os.path.abspath(path))
