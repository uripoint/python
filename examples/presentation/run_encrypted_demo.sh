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
DEPS=("ffmpeg" "python3" "openssl" "curl")
for dep in "${DEPS[@]}"; do
    if ! command -v $dep &> /dev/null; then
        print_error "$dep is required but not installed"
        exit 1
    fi
done

# Make scripts executable
chmod +x "$(dirname "$0")/setup_encrypted_video.sh"

# Clean any existing endpoints
print_status "Cleaning existing endpoints..."
uripoint --detach

# Setup encrypted video endpoints
print_status "Setting up encrypted video endpoints..."
"$(dirname "$0")/setup_encrypted_video.sh"

# Start the server
print_status "Starting UriPoint server..."
uripoint --serve &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Run encryption tests
print_status "Running encryption tests..."
python3 "$(dirname "$0")/test_encrypted_video.py"
TEST_STATUS=$?

if [ $TEST_STATUS -eq 0 ]; then
    print_success "Encryption tests passed!"
    
    # Start HTTP server for player
    print_status "Starting HTTP server for encrypted player..."
    HTTP_PORT=8080
    while nc -z localhost $HTTP_PORT 2>/dev/null; do
        HTTP_PORT=$((HTTP_PORT + 1))
    done
    
    python3 -m http.server $HTTP_PORT --directory "$(dirname "$0")" &
    HTTP_PID=$!
    
    print_success "Demo is running!"
    print_status "Access the encrypted player at: http://localhost:$HTTP_PORT/encrypted_player.html"
    print_status "Available streams:"
    echo "- Encrypted HLS: http://localhost:8000/encrypted/hls/master.m3u8"
    echo "- Encrypted DASH: http://localhost:8000/encrypted/dash/manifest.mpd"
    echo "- DRM License Server: http://localhost:8000/drm/license"
    print_status "Press Ctrl+C to stop the demo"
    
    # Save PIDs for cleanup
    echo $SERVER_PID > /tmp/uripoint_encrypted_demo.pid
    echo $HTTP_PID >> /tmp/uripoint_encrypted_demo.pid
    
    # Keep server running until interrupted
    wait $SERVER_PID
else
    print_error "Encryption tests failed!"
    kill $SERVER_PID
    exit 1
fi

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    if [ -f /tmp/uripoint_encrypted_demo.pid ]; then
        while read pid; do
            kill $pid 2>/dev/null
        done < /tmp/uripoint_encrypted_demo.pid
        rm /tmp/uripoint_encrypted_demo.pid
    fi
    
    # Clean up encryption keys
    if [ -d "$(dirname "$0")/keys" ]; then
        rm -rf "$(dirname "$0")/keys"
    fi
    
    # Clean up temporary files
    if [ -d "$(dirname "$0")/temp" ]; then
        rm -rf "$(dirname "$0")/temp"
    fi
    
    print_success "Cleanup complete"
}

# Set up cleanup on exit
trap cleanup EXIT

# Monitor key rotation
monitor_keys() {
    while true; do
        curl -s http://localhost:8000/keys/manage | jq .
        sleep 5
    done
}

# Start key monitoring in background
monitor_keys &
MONITOR_PID=$!
echo $MONITOR_PID >> /tmp/uripoint_encrypted_demo.pid
