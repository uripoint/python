#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

lsof -i:8080
lsof -i:8081
lsof -i:8082
lsof -i:8083
kill $(lsof -t -i:8080)
kill $(lsof -t -i:8081)
kill $(lsof -t -i:8082)
kill $(lsof -t -i:8083)
sleep 4


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
echo "http://localhost:8080/keys/hls.key" > "$KEYDIR/hls.keyinfo"

# Generate key for DASH encryption
print_status "Generating DASH encryption key..."
openssl rand 16 > "$KEYDIR/dash.key"
openssl rand 16 > "$KEYDIR/dash.iv"

# Create key endpoints
print_status "Creating key delivery endpoints..."

# HLS key endpoint
uripoint --uri http://localhost:8080/keys/hls.key --data "{
    \"response\": \"$(base64 "$KEYDIR/hls.key")\",
    \"content_type\": \"application/octet-stream\",
    \"headers\": {
        \"Access-Control-Allow-Origin\": \"*\"
    }
}" --method GET

# Create encrypted video endpoints
print_status "Creating encrypted video endpoints..."

# Encrypted HLS stream with key rotation
uripoint --uri http://localhost:8080/encrypted/hls/master.m3u8 --data '{
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size=1280x720:rate=30 -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v 2M -c:a aac -b:a 128k -hls_key_info_file '"${KEYDIR}/hls.keyinfo"' -hls_enc 1 -hls_time 4 -hls_list_size 5 -hls_flags delete_segments+periodic_rekey -f hls pipe:1",
    "content_type": "application/vnd.apple.mpegurl",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

print_success "Encrypted video endpoints created!"
echo "- Encrypted HLS: http://localhost:8080/encrypted/hls/master.m3u8"
echo "- Key Management: http://localhost:8080/keys/manage"
