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

# Generate encryption keys
KEYDIR="$(dirname "$0")/keys"
mkdir -p "$KEYDIR"

# Generate AES key for HLS
print_status "Generating HLS encryption key..."
openssl rand 16 > "$KEYDIR/hls.key"
echo "https://localhost:8080/keys/hls.key" > "$KEYDIR/hls.keyinfo"

# Generate key for DASH encryption
print_status "Generating DASH encryption key..."
openssl rand 16 > "$KEYDIR/dash.key"
openssl rand 16 > "$KEYDIR/dash.iv"

# Create key endpoints
print_status "Creating key delivery endpoints..."

# HLS key endpoint
uripoint --uri https://localhost:8080/keys/hls.key --data "{
    \"response\": \"$(base64 "$KEYDIR/hls.key")\",
    \"content_type\": \"application/octet-stream\",
    \"headers\": {
        \"Access-Control-Allow-Origin\": \"*\"
    }
}" --method GET

# Create encrypted video endpoints
print_status "Creating encrypted video endpoints..."

# Encrypted HLS stream with key rotation
uripoint --uri https://localhost:8080/encrypted/hls/master.m3u8 --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -hls_key_info_file '"${KEYDIR}/hls.keyinfo"' -hls_enc 1 -hls_time 4 -hls_list_size 5 -hls_flags delete_segments+periodic_rekey -f hls pipe:1",
    "content_type": "application/vnd.apple.mpegurl",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Encrypted DASH stream
uripoint --uri https://localhost:8080/encrypted/dash/manifest.mpd --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -encryption_scheme cenc-aes-ctr -encryption_key '"$(base64 "$KEYDIR/dash.key")"' -encryption_kid '"$(openssl rand -hex 16)"' -f dash -window_size 5 -extra_window_size 10 pipe:1",
    "content_type": "application/dash+xml",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Encrypted RTMP stream
print_status "Creating encrypted RTMP endpoint..."
uripoint --uri rtmp://localhost:1935/live/secure --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -aes_key '"$(base64 "$KEYDIR/rtmp.key")"' -aes_iv '"$(base64 "$KEYDIR/rtmp.iv")"' -f flv rtmp://localhost:1935/live/secure",
    "content_type": "video/x-flv",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}'

# Create DRM license server endpoint
print_status "Creating DRM license server..."
uripoint --uri https://localhost:8080/drm/license --data '{
    "response": {
        "keys": [{
            "kid": "'"$(openssl rand -hex 16)"'",
            "key": "'"$(base64 "$KEYDIR/dash.key")"'",
            "type": "temporary"
        }]
    },
    "content_type": "application/json",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method POST

# Create key management endpoint
print_status "Creating key management endpoint..."
uripoint --uri https://localhost:8080/keys/manage --data '{
    "response": {
        "rotation_interval": 300,
        "active_keys": [],
        "revoked_keys": []
    },
    "content_type": "application/json",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

print_success "Encrypted video endpoints created!"
print_status "Available endpoints:"
echo "- Encrypted HLS: https://localhost:8080/encrypted/hls/master.m3u8"
echo "- Encrypted DASH: https://localhost:8080/encrypted/dash/manifest.mpd"
echo "- Encrypted RTMP: rtmp://localhost:1935/live/secure"
echo "- DRM License: https://localhost:8080/drm/license"
echo "- Key Management: https://localhost:8080/keys/manage"

print_status "Start the server with: uripoint --serve"
