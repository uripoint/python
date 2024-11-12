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

# Create test video stream
print_status "Creating test video stream..."

# Create test pattern video
uripoint --uri http://localhost:8000/video/test --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -f mpegts pipe:1",
    "content_type": "video/MP2T",
    "headers": {
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Create webcam stream
print_status "Creating webcam stream..."
uripoint --uri http://localhost:8000/video/webcam --data '{
    "command": "ffmpeg -f v4l2 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -b:v 1M -f mpegts pipe:1",
    "content_type": "video/MP2T",
    "headers": {
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Create HLS stream endpoints
print_status "Creating HLS stream endpoints..."

# HLS master playlist
uripoint --uri http://localhost:8000/hls/master.m3u8 --data '{
    "response": {
        "content": "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1280x720\nhigh.m3u8\n#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=854x480\nmedium.m3u8\n#EXT-X-STREAM-INF:BANDWIDTH=500000,RESOLUTION=640x360\nlow.m3u8"
    },
    "content_type": "application/vnd.apple.mpegurl",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# High quality HLS stream
uripoint --uri http://localhost:8000/hls/high --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments pipe:1",
    "content_type": "application/vnd.apple.mpegurl",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Medium quality HLS stream
uripoint --uri http://localhost:8000/hls/medium --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=854x480:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 1M -c:a aac -b:a 96k -f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments pipe:1",
    "content_type": "application/vnd.apple.mpegurl",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Low quality HLS stream
uripoint --uri http://localhost:8000/hls/low --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=640x360:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 500k -c:a aac -b:a 64k -f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments pipe:1",
    "content_type": "application/vnd.apple.mpegurl",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Create DASH stream endpoints
print_status "Creating DASH stream endpoints..."

# DASH manifest
uripoint --uri http://localhost:8000/dash/manifest.mpd --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -f dash -window_size 5 -extra_window_size 10 pipe:1",
    "content_type": "application/dash+xml",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Create RTMP stream endpoint
print_status "Creating RTMP stream endpoint..."
uripoint --uri rtmp://localhost:1935/live/stream --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -f flv rtmp://localhost:1935/live/stream",
    "content_type": "video/x-flv",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}'

# Create stream status endpoint
print_status "Creating status endpoint..."
uripoint --uri http://localhost:8000/status --data '{
    "response": {
        "streams": {
            "test": "active",
            "webcam": "active",
            "hls": "active",
            "dash": "active",
            "rtmp": "active"
        },
        "viewers": {
            "test": 0,
            "webcam": 0,
            "hls": 0,
            "dash": 0,
            "rtmp": 0
        },
        "uptime": "0s",
        "bandwidth": "0 Mbps"
    }
}' --method GET

print_success "Video streaming endpoints created!"
print_status "Available endpoints:"
echo "- Test pattern: http://localhost:8000/video/test"
echo "- Webcam: http://localhost:8000/video/webcam"
echo "- HLS: http://localhost:8000/hls/master.m3u8"
echo "- DASH: http://localhost:8000/dash/manifest.mpd"
echo "- RTMP: rtmp://localhost:1935/live/stream"
echo "- Status: http://localhost:8000/status"

print_status "Start the server with: uripoint --serve"
