import pytest
import os
from uripoint.router import StreamFilterRouter, get_url_parts, extract_query_params, convert_file_path

def test_stream_filter_router():
    # Create router
    router = StreamFilterRouter()

    # Mock handler functions
    def status_handler(data):
        return {"status": "OK", "data": data}

    def user_handler(data):
        return {"user": "test", "data": data}

    # Add routes
    router.add_route(r'^/api/status$', status_handler)
    router.add_route(r'^/api/user/.*', user_handler)

    # Test route matching
    assert router.match_route('/api/status') is not None
    assert router.match_route('/api/user/profile') is not None
    assert router.match_route('/unknown') is None

    # Test route processing
    status_result = router.process('/api/status', 'test data')
    assert status_result == {"status": "OK", "data": "test data"}

    user_result = router.process('/api/user/profile', 'user data')
    assert user_result == {"user": "test", "data": "user data"}

def test_router_filters():
    router = StreamFilterRouter()

    # Filter to uppercase data
    def uppercase_filter(data):
        return data.upper() if isinstance(data, str) else data

    # Filter to add prefix
    def prefix_filter(data):
        return f"filtered: {data}" if isinstance(data, str) else data

    router.add_filter('uppercase', uppercase_filter)
    router.add_filter('prefix', prefix_filter)

    # Test filter application
    result = router.apply_filters("test data")
    assert result == "filtered: TEST DATA"

def test_url_parsing():
    # Test get_url_parts
    url = 'https://example.com/path?name=john&age=30#section'
    parts = get_url_parts(url)
    
    assert parts['scheme'] == 'https'
    assert parts['netloc'] == 'example.com'
    assert parts['path'] == '/path'
    assert parts['query']['name'] == ['john']
    assert parts['query']['age'] == ['30']
    assert parts['fragment'] == 'section'

def test_query_params():
    # Test extract_query_params
    url = 'https://example.com/search?q=python&category=programming'
    params = extract_query_params(url)
    
    assert params['q'] == ['python']
    assert params['category'] == ['programming']

def test_file_path_conversion():
    # Test convert_file_path
    base_dir = '/home/user/projects'
    
    # Test absolute path
    abs_path = convert_file_path('/tmp/test.txt')
    assert os.path.isabs(abs_path)
    assert abs_path.endswith('test.txt')

    # Test relative path with base directory
    rel_path = convert_file_path('test.txt', base_dir)
    assert rel_path.startswith(base_dir)
    assert rel_path.endswith('test.txt')

def test_router_error_handling():
    router = StreamFilterRouter()

    # Test processing with no matching route
    result = router.process('/unknown', 'data')
    assert result is None

    # Test processing with no filters
    result = router.apply_filters('test')
    assert result == 'test'
