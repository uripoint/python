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
DEPS=("ffmpeg" "python3" "curl")
for dep in "${DEPS[@]}"; do
    if ! command -v $dep &> /dev/null; then
        print_error "$dep is required but not installed"
        exit 1
    fi
done

# Make setup script executable
chmod +x "$(dirname "$0")/setup_video_endpoints.sh"

# Clean any existing endpoints
print_status "Cleaning existing endpoints..."
uripoint --detach

# Setup video endpoints
print_status "Setting up video endpoints..."
"$(dirname "$0")/setup_video_endpoints.sh"

# Start the server
print_status "Starting UriPoint server..."
uripoint --serve &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Run tests
print_status "Running endpoint tests..."
python3 "$(dirname "$0")/test_video_endpoints.py"
TEST_STATUS=$?

if [ $TEST_STATUS -eq 0 ]; then
    print_success "Tests completed successfully!"
    print_status "Video endpoints are ready to use."
    print_status "Press Ctrl+C to stop the server"
    
    # Keep server running until interrupted
    wait $SERVER_PID
else
    print_error "Tests failed!"
    kill $SERVER_PID
    exit 1
fi

# Cleanup on exit
trap 'kill $SERVER_PID 2>/dev/null' EXIT
