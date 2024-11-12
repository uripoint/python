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

# Function to check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check ffmpeg
    if ! command -v ffmpeg &> /dev/null; then
        print_error "ffmpeg is required but not installed"
        return 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "python3 is required but not installed"
        return 1
    fi

    return 0
}

# Function to check if a port is available
check_port() {
    nc -z localhost $1 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_error "Port $1 is already in use"
        return 1
    fi
    return 0
}

# Function to find available port
find_available_port() {
    local port=$1
    while nc -z localhost $port 2>/dev/null; do
        port=$((port + 1))
    done
    echo $port
}

# Function to clean existing endpoints
clean_endpoints() {
    print_status "Cleaning existing endpoints..."
    uripoint --detach
    sleep 1
}

# Function to setup test stream
setup_test_stream() {
    print_status "Setting up test stream..."
    
    # Create stream directory
    STREAM_DIR="$(dirname "$0")/stream"
    mkdir -p "$STREAM_DIR"
    echo $STREAM_DIR
    
    # Create test video with color bars and time overlay
    ffmpeg -y \
        -f lavfi -i "testsrc=duration=30:size=1280x720:rate=30" \
        -f lavfi -i "sine=frequency=1000:duration=30" \
        -vf "drawtext=text='%{pts\:hms}':box=1:x=(w-tw)/2:y=h-(2*lh):fontsize=72" \
        -c:v libx264 -preset ultrafast -b:v 3000k \
        -c:a aac -b:a 128k \
        "$STREAM_DIR/test_video.mp4"

    # Start HLS stream
    ffmpeg -y -re \
        -i "$STREAM_DIR/test_video.mp4" \
        -c:v copy \
        -c:a copy \
        -f hls \
        -hls_time 4 \
        -hls_list_size 5 \
        -hls_flags delete_segments \
        "$STREAM_DIR/stream.m3u8" &
    
    FFMPEG_PID=$!
    echo $FFMPEG_PID >> /tmp/uripoint_demo.pid
}

# Function to start the demo
start_demo() {
    print_status "Starting UriPoint Live Stream Demo..."

    # Check dependencies
    check_dependencies || exit 1

    # Clean existing endpoints
    clean_endpoints

    # Find available ports
    HTTP_PORT=$(find_available_port 8000)
    STREAM_PORT=$(find_available_port 8080)
    RTSP_PORT=$(find_available_port 8554)

    print_status "Using ports: HTTP=$HTTP_PORT, Stream=$STREAM_PORT, RTSP=$RTSP_PORT"

    # Setup test stream
    setup_test_stream

    # Create endpoints
    print_status "Creating stream endpoints..."
    uripoint --uri http://localhost:$STREAM_PORT/live/stream.m3u8 --data '{
        "response": {
            "type": "hls",
            "manifest_path": "stream/stream.m3u8"
        },
        "headers": {
            "Content-Type": "application/vnd.apple.mpegurl"
        }
    }' --method GET

    print_status "Creating status API..."
    uripoint --uri http://localhost:$STREAM_PORT/api/stream/status --data '{
        "response": {
            "status": "live",
            "viewers": 0,
            "uptime": "0s",
            "quality": "1080p"
        }
    }' --method GET

    print_status "Creating WebSocket chat..."
    uripoint --uri ws://localhost:$STREAM_PORT/chat --data '{
        "protocol": "chat",
        "max_connections": 100,
        "options": {
            "history_size": 50,
            "moderation": true
        }
    }'

    # Update player.html with correct ports
    print_status "Updating player configuration..."
    sed -i.bak "s/streamPort: [0-9]*/streamPort: $STREAM_PORT/g" "$(dirname "$0")/player.html"

    # Start UriPoint server
    print_status "Starting UriPoint server..."
    uripoint --serve &
    URIPOINT_PID=$!

    # Start Python HTTP server for the player
    print_status "Starting HTTP server for player..."
    python3 -m http.server $HTTP_PORT --directory "$(dirname "$0")" &
    HTTP_PID=$!

    # Save PIDs and ports for cleanup
    echo $URIPOINT_PID > /tmp/uripoint_demo.pid
    echo $HTTP_PID >> /tmp/uripoint_demo.pid
    echo "$HTTP_PORT:$STREAM_PORT:$RTSP_PORT" > /tmp/uripoint_demo.ports

    # Run stream tests
    print_status "Running stream tests..."
    python3 "$(dirname "$0")/test_stream.py"

    print_success "Demo is running!"
    print_status "Access the player at: http://localhost:$HTTP_PORT/player.html"
    print_status "Press Ctrl+C to stop the demo"

    # Wait for user interrupt
    wait
}

# Function to stop the demo
stop_demo() {
    print_status "Stopping demo..."
    
    # Kill processes
    if [ -f /tmp/uripoint_demo.pid ]; then
        while read pid; do
            kill $pid 2>/dev/null
        done < /tmp/uripoint_demo.pid
        rm /tmp/uripoint_demo.pid
    fi

    # Clean endpoints
    clean_endpoints

    # Restore original player.html
    if [ -f "$(dirname "$0")/player.html.bak" ]; then
        mv "$(dirname "$0")/player.html.bak" "$(dirname "$0")/player.html"
    fi

    # Clean stream files
    STREAM_DIR="$(dirname "$0")/stream"
    if [ -d "$STREAM_DIR" ]; then
        rm -rf "$STREAM_DIR"
    fi

    print_success "Demo stopped"
}

# Handle script interruption
trap stop_demo EXIT

# Main script
case "$1" in
    start)
        start_demo
        ;;
    stop)
        stop_demo
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

exit 0
