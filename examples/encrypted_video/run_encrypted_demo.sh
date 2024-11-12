#!/bin/bash
kill $(lsof -t -i:8080)
kill $(lsof -t -i:8081)
kill $(lsof -t -i:8082)
kill $(lsof -t -i:8083)
kill $(lsof -t -i:8084)
sleep 4

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

# Import Python config values
CONFIG_SCRIPT="
import sys
sys.path.append('.')
try:
    import config
    print(f'HOSTNAME={config.HOSTNAME}')
    print(f'URIPOINT_PORT={config.URIPOINT_PORT}')
    print(f'HTTP_PORT={config.HTTP_PORT}')
    print(f'KEY_DIR={config.KEY_DIR}')
    print(f'TEMP_DIR={config.TEMP_DIR}')
except Exception as e:
    print(f'Error importing config: {str(e)}', file=sys.stderr)
    sys.exit(1)
"

eval "$(python3 -c "$CONFIG_SCRIPT")" || {
    print_error "Failed to import configuration"
    exit 1
}

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

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
uripoint --serve --port $URIPOINT_PORT &
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
    python3 -m http.server $HTTP_PORT --directory "$(dirname "$0")" &
    HTTP_PID=$!
    
    print_success "Demo is running!"
    print_status "Access the encrypted player at: http://$HOSTNAME:$HTTP_PORT/encrypted_player.html"
    print_status "Available streams:"
    echo "- Encrypted HLS: http://$HOSTNAME:$URIPOINT_PORT/encrypted/hls/master.m3u8"
    echo "- Encrypted DASH: http://$HOSTNAME:$URIPOINT_PORT/encrypted/dash/manifest.mpd"
    echo "- DRM License Server: http://$HOSTNAME:$URIPOINT_PORT/drm/license"
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
    if [ -d "$(dirname "$0")/$KEY_DIR" ]; then
        rm -rf "$(dirname "$0")/$KEY_DIR"
    fi
    
    # Clean up temporary files
    if [ -d "$(dirname "$0")/$TEMP_DIR" ]; then
        rm -rf "$(dirname "$0")/$TEMP_DIR"
    fi
    
    print_success "Cleanup complete"
}

# Set up cleanup on exit
trap cleanup EXIT

# Monitor key rotation
monitor_keys() {
    while true; do
        curl -s http://$HOSTNAME:$URIPOINT_PORT/keys/manage | jq .
        sleep 5
    done
}

# Start key monitoring in background
monitor_keys &
MONITOR_PID=$!
echo $MONITOR_PID >> /tmp/uripoint_encrypted_demo.pid
