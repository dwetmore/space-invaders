FROM python:3.11-slim

WORKDIR /app

# Pygame + browser streaming stack.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgl1 \
        libx11-6 \
        libxext6 \
        libxrender1 \
        xvfb \
        x11vnc \
        novnc \
        websockify \
    && rm -rf /var/lib/apt/lists/*

COPY main.py /app/main.py
COPY scripts/start-novnc.sh /app/start-novnc.sh

RUN pip install --no-cache-dir pygame==2.6.1
RUN chmod +x /app/start-novnc.sh

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:1

EXPOSE 6080

CMD ["/app/start-novnc.sh"]
