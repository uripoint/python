# UriPoint Live Streaming Demo

## Scenario: Setting up a Multi-Protocol Live Stream System

### Step 1: Setup RTSP Camera Stream
```bash
# Create RTSP endpoint for camera feed
uripoint --uri rtsp://localhost:8554/camera1 --data '{
    "stream_url": "rtsp://camera.example.com/stream1",
    "transport": "tcp",
    "options": {
        "resolution": "1080p",
        "framerate": 30
    }
}'

# Test RTSP stream
ffplay rtsp://localhost:8554/camera1
```

### Step 2: Create HLS Stream
```bash
# Create HLS endpoint for web streaming
uripoint --uri http://localhost:8080/live/stream.m3u8 --data '{
    "manifest_url": "/live/stream.m3u8",
    "segment_duration": 4,
    "options": {
        "bandwidth_variants": [
            {"resolution": "1080p", "bitrate": 5000000},
            {"resolution": "720p", "bitrate": 2500000},
            {"resolution": "480p", "bitrate": 1000000}
        ]
    }
}'

# Test HLS stream
ffplay http://localhost:8080/live/stream.m3u8
```

### Step 3: Add Status API
```bash
# Create status endpoint
uripoint --uri http://localhost:8080/api/stream/status --data '{
    "response": {
        "status": "live",
        "viewers": 0,
        "uptime": "0s",
        "quality": "1080p"
    }
}' --method GET

# Monitor stream status
curl http://localhost:8080/api/stream/status
```

### Step 4: Create WebSocket Chat
```bash
# Create chat endpoint
uripoint --uri ws://localhost:8080/chat --data '{
    "protocol": "chat",
    "max_connections": 100,
    "options": {
        "history_size": 50,
        "moderation": true
    }
}'

# Test chat
wscat -c ws://localhost:8080/chat
```

## Live Demo Script

1. Start Camera Stream
```bash
# Terminal 1: Start UriPoint server
uripoint --serve

# Terminal 2: Start streaming
ffmpeg -i rtsp://camera.example.com/stream1 -c copy -f rtsp rtsp://localhost:8554/camera1
```

2. Launch Web Player
```html
<!-- stream.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Live Stream Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body>
    <video id="video" controls></video>
    <div id="chat"></div>
    <input id="message" type="text">
    <button onclick="sendMessage()">Send</button>

    <script>
        // HLS Player
        var video = document.getElementById('video');
        var hls = new Hls();
        hls.loadSource('http://localhost:8080/live/stream.m3u8');
        hls.attachMedia(video);

        // WebSocket Chat
        var ws = new WebSocket('ws://localhost:8080/chat');
        ws.onmessage = function(event) {
            var chat = document.getElementById('chat');
            chat.innerHTML += event.data + '<br>';
        };

        function sendMessage() {
            var input = document.getElementById('message');
            ws.send(input.value);
            input.value = '';
        }
    </script>
</body>
</html>
```

3. Monitor System
```bash
# Terminal 3: Monitor status
watch -n 1 'curl -s http://localhost:8080/api/stream/status'
```

## Presentation Flow

1. **Introduction (2 minutes)**
   - Explain UriPoint's purpose
   - Show architecture diagram
   - Highlight streaming capabilities

2. **Setup Demo (3 minutes)**
   - Create RTSP endpoint
   - Setup HLS streaming
   - Add status monitoring
   - Create chat system

3. **Live Demo (5 minutes)**
   - Start streaming server
   - Show video feed
   - Demonstrate chat functionality
   - Monitor system status

4. **Technical Deep Dive (5 minutes)**
   - Explain protocol handling
   - Show configuration options
   - Discuss scaling capabilities
   - Present error handling

5. **Q&A (5 minutes)**
   - Answer technical questions
   - Discuss use cases
   - Share best practices

## Key Points to Highlight

1. **Ease of Use**
   - Simple command-line interface
   - Quick endpoint creation
   - Automatic protocol handling

2. **Flexibility**
   - Multiple streaming protocols
   - Adaptive bitrate streaming
   - Real-time chat integration

3. **Monitoring**
   - Live status updates
   - Viewer statistics
   - System health checks

4. **Performance**
   - Low latency streaming
   - Efficient resource usage
   - Scalable architecture

## Common Questions

1. **How does it compare to traditional streaming servers?**
   - Lighter weight
   - Easier configuration
   - More flexible protocol support

2. **What about scaling?**
   - Supports multiple streams
   - Load balancing ready
   - Easy to cluster

3. **Security considerations?**
   - Authentication support
   - Encryption options
   - Access control

## Next Steps

1. **Documentation**
   - Share presentation slides
   - Provide example code
   - Link to GitHub repository

2. **Resources**
   - Installation guide
   - Configuration examples
   - Troubleshooting tips

3. **Support**
   - GitHub issues
   - Community chat
   - Email support
