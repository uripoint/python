# FFmpeg Examples with Environment Variables

20 examples of FFmpeg commands using environment variables (.env file) along with verification commands for each operation.

## Setup
`.env` file with common variables:

```bash
# .env file
INPUT_DIR=/path/to/input
OUTPUT_DIR=/path/to/output
STREAM_URL=rtmp://streaming-server/live
QUALITY_HIGH=4000k
QUALITY_MED=2000k
QUALITY_LOW=1000k
AUDIO_BITRATE=128k
SEGMENT_TIME=10
```

## Examples

### 1. Basic Video Transcoding
```bash
# Convert video to H.264/AAC format
ffmpeg -i ${INPUT_DIR}/input.mp4 -c:v libx264 -c:a aac -b:v ${QUALITY_HIGH} -b:a ${AUDIO_BITRATE} ${OUTPUT_DIR}/output.mp4

# Verify
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,bit_rate -of default=noprint_wrappers=1 ${OUTPUT_DIR}/output.mp4
```

### 2. HLS Stream Generation
```bash
# Create HLS stream with multiple qualities
ffmpeg -i ${INPUT_DIR}/input.mp4 \
    -map 0:v -map 0:a \
    -c:v libx264 -c:a aac \
    -b:v:0 ${QUALITY_HIGH} -b:v:1 ${QUALITY_MED} -b:v:2 ${QUALITY_LOW} \
    -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
    -master_pl_name master.m3u8 \
    -f hls -hls_time ${SEGMENT_TIME} \
    -hls_list_size 0 \
    -hls_segment_filename "${OUTPUT_DIR}/stream_%v/segment_%03d.ts" \
    ${OUTPUT_DIR}/stream_%v/playlist.m3u8

# Verify
curl -s ${OUTPUT_DIR}/master.m3u8 | grep -c "playlist.m3u8"
```

### 3. RTMP Stream Recording
```bash
# Record RTMP stream
ffmpeg -i ${STREAM_URL} -c copy ${OUTPUT_DIR}/stream_record.mp4

# Verify
ffprobe -v error -show_format -show_streams ${OUTPUT_DIR}/stream_record.mp4
```

### 4. Video Thumbnail Generation
```bash
# Generate thumbnails every 10 seconds
ffmpeg -i ${INPUT_DIR}/input.mp4 -vf fps=1/${SEGMENT_TIME} ${OUTPUT_DIR}/thumb_%03d.jpg

# Verify
find ${OUTPUT_DIR} -name "thumb_*.jpg" | wc -l
```

### 5. Audio Extraction
```bash
# Extract audio track
ffmpeg -i ${INPUT_DIR}/input.mp4 -vn -acodec libmp3lame -b:a ${AUDIO_BITRATE} ${OUTPUT_DIR}/audio.mp3

# Verify
ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1 ${OUTPUT_DIR}/audio.mp3
```

### 6. Video Compression
```bash
# Compress video with CRF
ffmpeg -i ${INPUT_DIR}/input.mp4 -c:v libx264 -crf 23 -c:a copy ${OUTPUT_DIR}/compressed.mp4

# Verify
ffprobe -v error -show_entries format=size -of default=noprint_wrappers=1 ${OUTPUT_DIR}/compressed.mp4
```

### 7. Video Watermarking
```bash
# Add watermark
ffmpeg -i ${INPUT_DIR}/input.mp4 -i ${INPUT_DIR}/watermark.png \
    -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10" \
    ${OUTPUT_DIR}/watermarked.mp4

# Verify
ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 ${OUTPUT_DIR}/watermarked.mp4
```

### 8. Video Resolution Scaling
```bash
# Scale video to 720p
ffmpeg -i ${INPUT_DIR}/input.mp4 -vf scale=-1:720 -c:v libx264 -c:a copy ${OUTPUT_DIR}/720p.mp4

# Verify
ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1 ${OUTPUT_DIR}/720p.mp4
```

### 9. GIF Creation
```bash
# Create GIF from video
ffmpeg -i ${INPUT_DIR}/input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v gif ${OUTPUT_DIR}/output.gif

# Verify
file ${OUTPUT_DIR}/output.gif
```

### 10. Video Trimming
```bash
# Trim video from 00:00:30 to 00:01:30
ffmpeg -i ${INPUT_DIR}/input.mp4 -ss 00:00:30 -t 00:01:00 -c copy ${OUTPUT_DIR}/trimmed.mp4

# Verify
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 ${OUTPUT_DIR}/trimmed.mp4
```

### 11. Audio Normalization
```bash
# Normalize audio levels
ffmpeg -i ${INPUT_DIR}/input.mp4 -filter:a loudnorm ${OUTPUT_DIR}/normalized.mp4

# Verify
ffmpeg -i ${OUTPUT_DIR}/normalized.mp4 -filter:a volumedetect -f null /dev/null 2>&1 | grep max_volume
```

### 12. Video Concatenation
```bash
# Concatenate multiple videos
ffmpeg -f concat -safe 0 -i ${INPUT_DIR}/filelist.txt -c copy ${OUTPUT_DIR}/concatenated.mp4

# Verify
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 ${OUTPUT_DIR}/concatenated.mp4
```

### 13. Screen Recording
```bash
# Record screen with audio
ffmpeg -f x11grab -video_size 1920x1080 -framerate 25 -i :0.0 \
    -f pulse -i default -c:v libx264 -c:a aac ${OUTPUT_DIR}/screen_recording.mp4

# Verify
ffprobe -v error -show_streams ${OUTPUT_DIR}/screen_recording.mp4
```

### 14. Video Rotation
```bash
# Rotate video 90 degrees clockwise
ffmpeg -i ${INPUT_DIR}/input.mp4 -vf "transpose=1" -c:a copy ${OUTPUT_DIR}/rotated.mp4

# Verify
ffprobe -v error -show_entries stream_tags=rotate -of default=noprint_wrappers=1 ${OUTPUT_DIR}/rotated.mp4
```

### 15. Audio Video Sync
```bash
# Fix audio/video sync issues
ffmpeg -i ${INPUT_DIR}/input.mp4 -itsoffset 1.0 -i ${INPUT_DIR}/input.mp4 \
    -map 0:v -map 1:a -c copy ${OUTPUT_DIR}/synced.mp4

# Verify
ffprobe -v error -show_entries stream=codec_type,start_time -of default=noprint_wrappers=1 ${OUTPUT_DIR}/synced.mp4
```

### 16. Video Stabilization
```bash
# Stabilize shaky video
ffmpeg -i ${INPUT_DIR}/input.mp4 -vf deshake ${OUTPUT_DIR}/stabilized.mp4

# Verify
ffmpeg -i ${OUTPUT_DIR}/stabilized.mp4 -vf freezedetect -f null - 2>&1 | grep freeze_
```

### 17. Subtitles Burning
```bash
# Burn subtitles into video
ffmpeg -i ${INPUT_DIR}/input.mp4 -vf subtitles=${INPUT_DIR}/subs.srt ${OUTPUT_DIR}/with_subs.mp4

# Verify
ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1 ${OUTPUT_DIR}/with_subs.mp4
```

### 18. Video Speed Adjustment
```bash
# Speed up video by 2x
ffmpeg -i ${INPUT_DIR}/input.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" ${OUTPUT_DIR}/fast.mp4

# Verify
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 ${OUTPUT_DIR}/fast.mp4
```

### 19. Multi-Stream Output
```bash
# Output to multiple streaming services simultaneously
ffmpeg -i ${INPUT_DIR}/input.mp4 \
    -c:v libx264 -c:a aac \
    -b:v ${QUALITY_HIGH} \
    -f tee \
    "[f=flv]${STREAM_URL}_1|[f=flv]${STREAM_URL}_2"

# Verify
ffprobe -v error ${STREAM_URL}_1 2>&1 | grep "Connection refused" || echo "Stream 1 is active"
```

### 20. Video Quality Assessment
```bash
# Calculate PSNR/SSIM metrics
ffmpeg -i ${INPUT_DIR}/original.mp4 -i ${INPUT_DIR}/encoded.mp4 \
    -lavfi "ssim;[0:v][1:v]psnr" -f null - 2> ${OUTPUT_DIR}/quality_metrics.txt

# Verify
cat ${OUTPUT_DIR}/quality_metrics.txt | grep -E "SSIM|PSNR"
```

## Environment Variables Usage

To use these commands:

1. Create a `.env` file in your project directory
2. Add the necessary environment variables
3. Source the environment file before running commands:
```bash
source .env
```

## Notes

- Always verify output files/streams after processing
- Check logs for any errors or warnings
- Monitor system resources during processing
- Adjust bitrates and quality settings based on your needs
- Keep backup copies of original files