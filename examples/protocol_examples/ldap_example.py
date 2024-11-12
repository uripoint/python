"""
Example demonstrating LDAP protocol support in UriPoint
"""
from uripoint import UriPointCLI

def setup_ldap_endpoints():
    """Setup LDAP directory endpoints"""
    cli = UriPointCLI()

    # LDAP authentication endpoint
    cli.create_endpoint(
        uri='ldap://localhost:389/dc=example,dc=com',
        data={
            'server_type': 'openldap',
            'schema': {
                'objectClasses': [
                    'top',
                    'person',
                    'organizationalPerson',
                    'inetOrgPerson'
                ],
                'attributes': [
                    'uid',
                    'cn',
                    'sn',
                    'givenName',
                    'mail',
                    'userPassword'
                ]
            },
            'bind': {
                'dn': 'cn=admin,dc=example,dc=com',
                'method': 'simple'
            },
            'options': {
                'tls': True,
                'version': 3,
                'timeout': 30
            }
        }
    )

    # User directory endpoint
    cli.create_endpoint(
        uri='ldap://localhost:389/ou=users,dc=example,dc=com',
        data={
            'operations': ['search', 'add', 'modify', 'delete'],
            'attributes': {
                'required': ['uid', 'cn', 'sn', 'mail'],
                'optional': ['telephoneNumber', 'title', 'manager']
            },
            'indexes': ['uid', 'mail'],
            'acl': [
                {
                    'who': 'cn=admin,dc=example,dc=com',
                    'access': '*'
                },
                {
                    'who': '*',
                    'access': 'read'
                }
            ]
        }
    )

    # Group directory endpoint
    cli.create_endpoint(
        uri='ldap://localhost:389/ou=groups,dc=example,dc=com',
        data={
            'objectClass': ['top', 'groupOfNames'],
            'attributes': {
                'required': ['cn', 'member'],
                'optional': ['description']
            },
            'operations': ['search', 'add', 'modify'],
            'acl': [
                {
                    'who': 'cn=admin,dc=example,dc=com',
                    'access': '*'
                },
                {
                    'who': 'self',
                    'access': 'read,search'
                }
            ]
        }
    )

    # Organization units endpoint
    cli.create_endpoint(
        uri='ldap://localhost:389/ou=departments,dc=example,dc=com',
        data={
            'objectClass': ['top', 'organizationalUnit'],
            'attributes': {
                'required': ['ou'],
                'optional': ['description', 'manager']
            },
            'operations': ['search'],
            'structure': {
                'ou=engineering': {
                    'ou=development': {},
                    'ou=qa': {},
                    'ou=devops': {}
                },
                'ou=sales': {},
                'ou=marketing': {},
                'ou=hr': {}
            }
        }
    )

    print("\nLDAP endpoints created:")
    print("1. Authentication:")
    print("   - URI: ldap://localhost:389/dc=example,dc=com")
    print("   - Type: OpenLDAP")
    print("   - Version: 3")
    
    print("\n2. User Directory:")
    print("   - URI: ldap://localhost:389/ou=users,dc=example,dc=com")
    print("   - Operations: search, add, modify, delete")
    print("   - Required Attributes: uid, cn, sn, mail")
    
    print("\n3. Group Directory:")
    print("   - URI: ldap://localhost:389/ou=groups,dc=example,dc=com")
    print("   - Type: groupOfNames")
    print("   - Operations: search, add, modify")
    
    print("\n4. Organization Units:")
    print("   - URI: ldap://localhost:389/ou=departments,dc=example,dc=com")
    print("   - Type: organizationalUnit")
    print("   - Structure: engineering, sales, marketing, hr")

def test_ldap_operations():
    """Test LDAP directory operations"""
    cli = UriPointCLI()

    # Add user
    print("\nAdding new user...")
    user_data = {
        'objectClass': ['inetOrgPerson'],
        'uid': 'jdoe',
        'cn': 'John Doe',
        'sn': 'Doe',
        'givenName': 'John',
        'mail': 'john.doe@example.com',
        'userPassword': '{SSHA}encrypted_password_hash'
    }
    cli.publish('ldap://localhost:389/ou=users,dc=example,dc=com', user_data)

    # Search users
    print("\nSearching for users...")
    search_filter = '(&(objectClass=inetOrgPerson)(mail=*@example.com))'
    cli.search('ldap://localhost:389/ou=users,dc=example,dc=com', 
              {'filter': search_filter, 'scope': 'sub'})

    # Add group
    print("\nCreating new group...")
    group_data = {
        'objectClass': ['groupOfNames'],
        'cn': 'developers',
        'description': 'Development team',
        'member': ['uid=jdoe,ou=users,dc=example,dc=com']
    }
    cli.publish('ldap://localhost:389/ou=groups,dc=example,dc=com', group_data)

    # Modify user
    print("\nModifying user attributes...")
    modify_data = {
        'operation': 'modify',
        'changes': {
            'add': {'telephoneNumber': '+1234567890'},
            'replace': {'title': 'Senior Developer'},
            'delete': ['description']
        }
    }
    cli.modify('ldap://localhost:389/uid=jdoe,ou=users,dc=example,dc=com', modify_data)

def setup_ldap_options():
    """Configure LDAP protocol options"""
    return {
        'security': {
            'tls': True,
            'start_tls': True,
            'verify_cert': True,
            'ca_cert_file': '/path/to/ca.crt'
        },
        'connection': {
            'timeout': 30,
            'keep_alive': True,
            'pool_size': 10
        },
        'operation': {
            'page_size': 100,
            'size_limit': 1000,
            'time_limit': 30
        },
        'authentication': {
            'sasl_mechanisms': ['DIGEST-MD5', 'GSSAPI'],
            'tls_ciphers': 'HIGH:-SSLv2'
        }
    }

if __name__ == '__main__':
    print("Setting up LDAP endpoints...")
    setup_ldap_endpoints()
    
    print("\nTesting LDAP operations...")
    test_ldap_operations()
