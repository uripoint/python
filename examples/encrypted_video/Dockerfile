FROM python:3.9-slim

# Install system dependencies including FFmpeg and OpenSSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for keys and temp files
RUN mkdir -p keys temp

# Make setup script executable
RUN chmod +x setup_encrypted_video.sh

# Set environment variables with defaults
ENV URIPOINT_HOST=0.0.0.0 \
    URIPOINT_PORT=8083 \
    HTTP_PORT=8082 \
    FFMPEG_VIDEO_SIZE=1280x720 \
    FFMPEG_FRAME_RATE=30 \
    FFMPEG_VIDEO_BITRATE=2M \
    FFMPEG_AUDIO_BITRATE=128k \
    FFMPEG_HLS_TIME=4 \
    FFMPEG_HLS_LIST_SIZE=5 \
    KEY_ROTATION_INTERVAL=300

# Expose ports
EXPOSE 8082 8083

# Run the setup script and start the server
CMD ["bash", "-c", "./setup_encrypted_video.sh && uripoint --serve"]
