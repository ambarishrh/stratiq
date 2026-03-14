#!/bin/bash
cd "$(dirname "$0")"
echo "Starting StratIQ..."
docker pull ambarishrh/stratiq:latest 2>/dev/null || true
docker stop stratiq 2>/dev/null || true
docker rm stratiq 2>/dev/null || true
docker run -d \
  -p 3000:3000 \
  --add-host=host.docker.internal:host-gateway \
  -v stratiq_data:/app/data \
  --name stratiq \
  ambarishrh/stratiq:latest
echo "StratIQ running at http://localhost:3000"
open http://localhost:3000
