FROM python:3.12-slim

LABEL maintainer="Adrian Fudge"
LABEL description="Merge-Tactics-AI: Reinforcement learning environment for Merge Tactics agent"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    python3-dev \
    build-essential \
    libx11-6 \
    libxtst6 \
    libpng16-16 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY env.py agent.py actions.py train.py test.py analyze_metrics.py ./
COPY models/ models/
COPY main_images/ main_images/
COPY screenshots/ screenshots/

RUN chmod -R 777 screenshots

# Default behavior: run training with fake display
CMD ["xvfb-run", "-a", "python", "train.py"]
