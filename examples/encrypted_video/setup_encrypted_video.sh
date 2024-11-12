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
    print(f'FFMPEG_VIDEO_SIZE={config.FFMPEG_SETTINGS[\"video_size\"]}')
    print(f'FFMPEG_FRAME_RATE={config.FFMPEG_SETTINGS[\"frame_rate\"]}')
    print(f'FFMPEG_VIDEO_BITRATE={config.FFMPEG_SETTINGS[\"video_bitrate\"]}')
    print(f'FFMPEG_AUDIO_BITRATE={config.FFMPEG_SETTINGS[\"audio_bitrate\"]}')
    print(f'FFMPEG_HLS_TIME={config.FFMPEG_SETTINGS[\"hls_time\"]}')
    print(f'FFMPEG_HLS_LIST_SIZE={config.FFMPEG_SETTINGS[\"hls_list_size\"]}')
    print(f'KEY_ROTATION_INTERVAL={config.KEY_ROTATION_INTERVAL}')
except Exception as e:
    print(f'Error importing config: {str(e)}', file=sys.stderr)
    sys.exit(1)
"

eval "$(python3 -c "$CONFIG_SCRIPT")" || {
    print_error "Failed to import configuration"
    exit 1
}

# Generate encryption keys
KEYDIR="$(dirname "$0")/$KEY_DIR"
mkdir -p "$KEYDIR"

# Generate AES key for HLS
print_status "Generating HLS encryption key..."
openssl rand 16 > "$KEYDIR/hls.key"
echo "http://$HOSTNAME:$URIPOINT_PORT/keys/hls.key" > "$KEYDIR/hls.keyinfo"

# Generate key for DASH encryption
print_status "Generating DASH encryption key..."
openssl rand 16 > "$KEYDIR/dash.key"
openssl rand 16 > "$KEYDIR/dash.iv"

# Create key endpoints
print_status "Creating key delivery endpoints..."

# HLS key endpoint
uripoint --uri http://$HOSTNAME:$URIPOINT_PORT/keys/hls.key --data "{
    \"response\": \"$(base64 "$KEYDIR/hls.key")\",
    \"content_type\": \"application/octet-stream\",
    \"headers\": {
        \"Access-Control-Allow-Origin\": \"*\"
    }
}" --method GET

# Create encrypted video endpoints
print_status "Creating encrypted video endpoints..."

# Encrypted HLS stream with key rotation
uripoint --uri http://$HOSTNAME:$URIPOINT_PORT/encrypted/hls/master.m3u8 --data '{
    "response": "",
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size='"$FFMPEG_VIDEO_SIZE"':rate='"$FFMPEG_FRAME_RATE"' -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v '"$FFMPEG_VIDEO_BITRATE"' -c:a aac -b:a '"$FFMPEG_AUDIO_BITRATE"' -hls_key_info_file '"${KEYDIR}/hls.keyinfo"' -hls_enc 1 -hls_time '"$FFMPEG_HLS_TIME"' -hls_list_size '"$FFMPEG_HLS_LIST_SIZE"' -hls_flags delete_segments+periodic_rekey -f hls pipe:1",
    "content_type": "application/vnd.apple.mpegurl",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Encrypted DASH stream
uripoint --uri http://$HOSTNAME:$URIPOINT_PORT/encrypted/dash/manifest.mpd --data '{
    "response": "",
    "command": "ffmpeg -f lavfi -i testsrc=duration=3600:size='"$FFMPEG_VIDEO_SIZE"':rate='"$FFMPEG_FRAME_RATE"' -f lavfi -i sine=frequency=1000:duration=3600 -c:v libx264 -preset ultrafast -b:v '"$FFMPEG_VIDEO_BITRATE"' -c:a aac -b:a '"$FFMPEG_AUDIO_BITRATE"' -encryption_scheme cenc-aes-ctr -encryption_key '"$(base64 "$KEYDIR/dash.key")"' -encryption_kid '"$(openssl rand -hex 16)"' -f dash -window_size 5 -extra_window_size 10 pipe:1",
    "content_type": "application/dash+xml",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}' --method GET

# Create DRM license server endpoint
print_status "Creating DRM license server..."
uripoint --uri http://$HOSTNAME:$URIPOINT_PORT/drm/license --data '{
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
uripoint --uri http://$HOSTNAME:$URIPOINT_PORT/keys/manage --data '{
    "response": {
        "rotation_interval": '"$KEY_ROTATION_INTERVAL"',
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
echo "- Encrypted HLS: http://$HOSTNAME:$URIPOINT_PORT/encrypted/hls/master.m3u8"
echo "- Encrypted DASH: http://$HOSTNAME:$URIPOINT_PORT/encrypted/dash/manifest.mpd"
echo "- DRM License: http://$HOSTNAME:$URIPOINT_PORT/drm/license"
echo "- Key Management: http://$HOSTNAME:$URIPOINT_PORT/keys/manage"

print_status "Start the server with: uripoint --serve"
