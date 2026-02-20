FROM python:3.11-slim

WORKDIR /app

# Pygame needs SDL runtime libraries; dummy video driver allows running headless in pods.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libglib2.0-0 libgl1 libx11-6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY main.py /app/main.py

RUN pip install --no-cache-dir pygame==2.6.1

ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy
ENV PYTHONUNBUFFERED=1

CMD ["python", "/app/main.py"]
