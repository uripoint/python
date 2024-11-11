#!/bin/bash

# HTTP Endpoint
uripoint --uri /api/status --protocol http --port 8000 --data '{"status": "OK"}'

# FTP Endpoint
uripoint --uri /files --protocol ftp --port 2121 --data '{"directory": "./files"}'

# RTSP Endpoint
uripoint --uri /stream --protocol rtsp --port 8554 --data '{"stream_name": "test"}'

# List all endpoints
uripoint --list

# Serve all endpoints
uripoint --serve
