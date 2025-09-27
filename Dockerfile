FROM python:3.9-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kor \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 모든 파일 복사
COPY . .

# pip 업그레이드 및 Python 패키지 설치
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 8501

# 앱 실행
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
