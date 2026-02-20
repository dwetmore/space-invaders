#!/usr/bin/env bash
set -euo pipefail

export DISPLAY=:1

Xvfb :1 -screen 0 1024x768x24 &
x11vnc -display :1 -forever -shared -rfbport 5900 -nopw -listen 0.0.0.0 &
websockify --web /usr/share/novnc 6080 localhost:5900 &

exec python /app/main.py
