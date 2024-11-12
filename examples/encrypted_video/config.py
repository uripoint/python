"""
Configuration variables for encrypted video demo
"""
import os

# Server configuration
HOSTNAME = os.getenv('URIPOINT_HOST', 'localhost')
URIPOINT_PORT = int(os.getenv('URIPOINT_PORT', '8083'))
HTTP_PORT = int(os.getenv('HTTP_PORT', '8082'))

# URL construction
BASE_URL = f'http://{HOSTNAME}:{URIPOINT_PORT}'
HTTP_BASE_URL = f'http://{HOSTNAME}:{HTTP_PORT}'

# Endpoint paths
ENDPOINTS = {
    'hls_key': f'{BASE_URL}/keys/hls.key',
    'hls_master': f'{BASE_URL}/encrypted/hls/master.m3u8',
    'dash_manifest': f'{BASE_URL}/encrypted/dash/manifest.mpd',
    'drm_license': f'{BASE_URL}/drm/license',
    'key_manage': f'{BASE_URL}/keys/manage',
    'player': f'{HTTP_BASE_URL}/encrypted_player.html'
}

# Directory paths
KEY_DIR = 'keys'
TEMP_DIR = 'temp'

# FFmpeg settings
FFMPEG_SETTINGS = {
    'video_size': '1280x720',
    'frame_rate': '30',
    'video_bitrate': '2M',
    'audio_bitrate': '128k',
    'hls_time': '4',
    'hls_list_size': '5'
}

# Key rotation settings
KEY_ROTATION_INTERVAL = 300  # seconds
