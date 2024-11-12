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

# Check dependencies
print_status "Checking dependencies..."
DEPS=("openssl" "python3" "curl" "ffmpeg")
for dep in "${DEPS[@]}"; do
    if ! command -v $dep &> /dev/null; then
        print_error "$dep is required but not installed"
        exit 1
    fi
done

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -q requests jwt websockets cryptography

# Make scripts executable
chmod +x "$(dirname "$0")/setup_security.sh"

# Clean any existing endpoints
print_status "Cleaning existing endpoints..."
uripoint --detach

# Setup security endpoints
print_status "Setting up security endpoints..."
"$(dirname "$0")/setup_security.sh"

# Start the secure server
print_status "Starting secure UriPoint server..."
uripoint --serve --tls &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Run security tests
print_status "Running security tests..."
python3 "$(dirname "$0")/test_security.py"
TEST_STATUS=$?

if [ $TEST_STATUS -eq 0 ]; then
    print_success "Security tests passed!"
    
    print_status "Security features enabled:"
    echo "- Input validation"
    echo "- JWT authentication"
    echo "- Process sandboxing"
    echo "- Network security (firewall, rate limiting)"
    echo "- TLS 1.2/1.3 encryption"
    echo "- Protocol-specific security"
    
    print_status "Available endpoints:"
    echo "- Authentication: https://localhost:8000/auth/token"
    echo "- Validation: https://localhost:8000/validate"
    echo "- Process Management: https://localhost:8000/process/manage"
    echo "- Network Security: https://localhost:8000/security/network"
    echo "- TLS Configuration: https://localhost:8000/security/tls"
    echo "- Security Monitor: https://localhost:8000/security/monitor"
    
    print_status "Security monitoring active. Press Ctrl+C to stop."
    
    # Start security monitoring
    monitor_security() {
        while true; do
            echo -e "\nSecurity Status ($(date)):"
            curl -sk https://localhost:8000/security/monitor | jq .
            sleep 5
        done
    }
    
    monitor_security &
    MONITOR_PID=$!
    
    # Save PIDs for cleanup
    echo $SERVER_PID > /tmp/uripoint_security_demo.pid
    echo $MONITOR_PID >> /tmp/uripoint_security_demo.pid
    
    # Keep server running until interrupted
    wait $SERVER_PID
else
    print_error "Security tests failed!"
    kill $SERVER_PID
    exit 1
fi

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    if [ -f /tmp/uripoint_security_demo.pid ]; then
        while read pid; do
            kill $pid 2>/dev/null
        done < /tmp/uripoint_security_demo.pid
        rm /tmp/uripoint_security_demo.pid
    fi
    
    # Clean up SSL certificates
    if [ -d "$(dirname "$0")/ssl" ]; then
        rm -rf "$(dirname "$0")/ssl"
    fi
    
    print_success "Cleanup complete"
}

# Set up cleanup on exit
trap cleanup EXIT

# Display security logs
tail_logs() {
    while true; do
        if [ -f "$(dirname "$0")/security.log" ]; then
            tail -f "$(dirname "$0")/security.log"
        fi
        sleep 1
    done
}

# Start log monitoring in background
tail_logs &
LOG_PID=$!
echo $LOG_PID >> /tmp/uripoint_security_demo.pid
