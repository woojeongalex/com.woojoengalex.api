# 1. 가볍고 안정적인 파이썬 3.13 환경을 가져옵니다
FROM python:3.13-slim

# 2. 컨테이너 내부에서 작업할 폴더 지정
WORKDIR /app

# 2-1. opencv-python-headless 실행에 필요한 최소 시스템 라이브러리
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 3. 의존성 패키지 설치 (캐시 최적화를 위해 먼저 복사)
COPY requirements.txt .
RUN grep -v -E '^--extra-index-url|^torch==|^torchvision==|^torchaudio==' requirements.txt > /tmp/req_notorch.txt && \
    pip install --no-cache-dir -r /tmp/req_notorch.txt && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 4. 백엔드 폴더 안의 모든 파일(apps, core, main.py 등)을 복사
COPY . .

# 5. FastAPI 서버 실행 (main.py 호출)
CMD ["python", "main.py"]
