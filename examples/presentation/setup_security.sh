#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Function to print colored status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Generate SSL certificates
print_status "Generating SSL certificates..."
SSL_DIR="$(dirname "$0")/ssl"
mkdir -p "$SSL_DIR"

openssl req -x509 -newkey rsa:4096 -keyout "$SSL_DIR/key.pem" -out "$SSL_DIR/cert.pem" -days 365 -nodes \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
    -addext "subjectAltName = DNS:localhost,IP:127.0.0.1"

# Create authentication endpoint
print_status "Creating authentication endpoint..."
uripoint --uri https://localhost:8000/auth/token --data '{
    "validator": {
        "type": "jwt",
        "secret": "'"$(openssl rand -base64 32)"'",
        "expiry": 3600
    },
    "rate_limit": {
        "requests": 10,
        "per_seconds": 60
    },
    "headers": {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Content-Security-Policy": "default-src '\''self'\''"
    }
}' --method POST

# Create input validation endpoint
print_status "Creating input validation endpoint..."
uripoint --uri https://localhost:8000/validate --data '{
    "validators": {
        "username": "^[a-zA-Z0-9_]{3,16}$",
        "email": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
        "password": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
    },
    "sanitizers": {
        "html": true,
        "sql": true,
        "xss": true
    }
}' --method POST

# Create secure process management endpoint
print_status "Creating process management endpoint..."
uripoint --uri https://localhost:8000/process/manage --data '{
    "allowed_processes": ["ffmpeg", "python3"],
    "resource_limits": {
        "cpu_percent": 80,
        "memory_mb": 1024,
        "max_processes": 10
    },
    "security": {
        "chroot": true,
        "no_network": false,
        "readonly_fs": true
    }
}' --method POST

# Create network security endpoint
print_status "Creating network security endpoint..."
uripoint --uri https://localhost:8000/security/network --data '{
    "firewall": {
        "allowed_ips": ["127.0.0.1"],
        "allowed_ports": [8000, 8080, 8443],
        "blocked_ranges": ["0.0.0.0/0"]
    },
    "ddos_protection": {
        "rate_limit": 100,
        "burst": 10,
        "ban_duration": 300
    },
    "tls": {
        "min_version": "1.2",
        "ciphers": "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256"
    }
}' --method POST

# Create protocol-specific security endpoints
print_status "Creating protocol security endpoints..."

# HTTPS security
uripoint --uri https://localhost:8000/security/https --data '{
    "hsts": true,
    "csp": "default-src '\''self'\''",
    "xss_protection": true,
    "frame_options": "DENY",
    "cert_pinning": true
}' --method POST

# RTMP security
uripoint --uri https://localhost:8000/security/rtmp --data '{
    "authentication": true,
    "token_validation": true,
    "ip_restriction": true,
    "stream_key": "'"$(openssl rand -hex 32)"'"
}' --method POST

# WebSocket security
uripoint --uri wss://localhost:8000/security/ws --data '{
    "origin_check": true,
    "message_validation": true,
    "max_connections": 100,
    "timeout": 30
}' --method POST

# Create TLS configuration endpoint
print_status "Creating TLS configuration endpoint..."
uripoint --uri https://localhost:8000/security/tls --data '{
    "protocols": ["TLSv1.2", "TLSv1.3"],
    "ciphers": [
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256"
    ],
    "certificate": "'"$(base64 "$SSL_DIR/cert.pem")"'",
    "key": "'"$(base64 "$SSL_DIR/key.pem")"'",
    "options": {
        "session_tickets": false,
        "stapling": true,
        "hsts": true
    }
}' --method POST

# Create security monitoring endpoint
print_status "Creating security monitoring endpoint..."
uripoint --uri https://localhost:8000/security/monitor --data '{
    "metrics": {
        "auth_failures": 0,
        "blocked_ips": [],
        "active_sessions": 0,
        "tls_handshakes": 0
    },
    "alerts": {
        "auth_threshold": 5,
        "ddos_threshold": 1000,
        "brute_force_threshold": 10
    }
}' --method GET

print_success "Security endpoints created!"
print_status "Available security endpoints:"
echo "- Authentication: https://localhost:8000/auth/token"
echo "- Input Validation: https://localhost:8000/validate"
echo "- Process Management: https://localhost:8000/process/manage"
echo "- Network Security: https://localhost:8000/security/network"
echo "- Protocol Security: https://localhost:8000/security/{https,rtmp,ws}"
echo "- TLS Configuration: https://localhost:8000/security/tls"
echo "- Security Monitor: https://localhost:8000/security/monitor"

print_status "Start the secure server with: uripoint --serve --tls"
