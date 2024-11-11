"""
DNS Protocol Example for UriPoint
Demonstrates domain name resolution and DNS record management
"""

from uripoint import UriPointCLI

def setup_dns_endpoints():
    # Create CLI instance
    cli = UriPointCLI()

    # Create DNS endpoint for domain lookups
    cli.create_endpoint(
        uri='dns://8.8.8.8:53/lookup',
        data={
            'timeout': 5,
            'retries': 3,
            'cache_enabled': True,
            'cache_ttl': 300  # 5 minutes
        }
    )

    # Create DNS endpoint for reverse lookups
    cli.create_endpoint(
        uri='dns://8.8.8.8:53/reverse',
        data={
            'timeout': 5,
            'retries': 3,
            'cache_enabled': True,
            'cache_ttl': 300
        }
    )

def demonstrate_dns_operations():
    cli = UriPointCLI()
    
    # Perform forward DNS lookup
    domain_query = {
        'domain': 'example.com',
        'record_type': 'A',
        'recursive': True
    }
    
    result = cli.query('dns://8.8.8.8:53/lookup', domain_query)
    print(f"DNS lookup result: {result}")
    
    # Perform reverse DNS lookup
    ip_query = {
        'ip': '93.184.216.34',  # example.com IP
        'validate': True
    }
    
    result = cli.query('dns://8.8.8.8:53/reverse', ip_query)
    print(f"Reverse DNS lookup result: {result}")

def check_dns_records():
    cli = UriPointCLI()
    
    # Query different DNS record types
    records_to_check = [
        {'domain': 'example.com', 'type': 'MX'},
        {'domain': 'example.com', 'type': 'TXT'},
        {'domain': 'example.com', 'type': 'NS'},
        {'domain': '_sip._tcp.example.com', 'type': 'SRV'}
    ]
    
    for record in records_to_check:
        query = {
            'domain': record['domain'],
            'record_type': record['type'],
            'recursive': True
        }
        
        result = cli.query('dns://8.8.8.8:53/lookup', query)
        print(f"{record['type']} records for {record['domain']}: {result}")

def monitor_dns_changes():
    cli = UriPointCLI()
    
    def dns_change_callback(change):
        print(f"DNS record change detected: {change}")
    
    # Monitor specific domain for changes
    monitor_config = {
        'domain': 'example.com',
        'record_types': ['A', 'AAAA', 'MX'],
        'interval': 300,  # Check every 5 minutes
        'callback': dns_change_callback
    }
    
    cli.monitor('dns://8.8.8.8:53/lookup', monitor_config)

if __name__ == '__main__':
    setup_dns_endpoints()
    demonstrate_dns_operations()
    check_dns_records()
    monitor_dns_changes()
