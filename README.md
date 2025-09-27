# 📄 PDF OCR 도구

PDF 파일을 업로드하면 자동으로 텍스트를 추출하는 웹 애플리케이션입니다.

## ✨ 주요 기능

- 📄 **PDF → 텍스트 변환**: PDF 파일을 이미지로 변환 후 OCR 처리
- 🌍 **다국어 지원**: 한국어, 영어, 일본어, 중국어 등 163개 언어 지원
- 🎨 **웹 인터페이스**: Streamlit 기반의 직관적인 UI/UX
- 📊 **실시간 처리**: 진행률 표시와 함께 OCR 처리
- 📋 **결과 표시**: 전체 텍스트와 페이지별 텍스트로 구분
- 💾 **다운로드**: 개별 텍스트 파일 또는 ZIP 파일로 다운로드

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
# macOS
brew install tesseract tesseract-lang poppler

# Ubuntu/Debian
sudo apt-get install -y tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng poppler-utils

# CentOS/RHEL
sudo yum install -y tesseract tesseract-langpack-kor poppler-utils
```

### 2. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 실행

```bash
# Streamlit 앱 실행
streamlit run app.py

# 또는 Flask 앱 실행
python3 web_ocr.py
```

## 📱 사용 방법

1. 웹 브라우저에서 `http://localhost:8501` 접속
2. PDF 파일 업로드 (드래그 앤 드롭 또는 클릭)
3. 언어 선택 (한국어+영어 권장)
4. "OCR 실행" 버튼 클릭
5. 결과 확인 및 다운로드

## 🛠️ 기술 스택

- **Backend**: Python, Streamlit, Flask
- **OCR**: Tesseract OCR
- **PDF 처리**: pdf2image, poppler
- **Frontend**: HTML, CSS, JavaScript

## 📁 프로젝트 구조

```
ocr2/
├── app.py                 # Streamlit 메인 앱
├── web_ocr.py            # Flask 웹 앱
├── pdf_ocr.py            # CLI OCR 스크립트
├── templates/
│   └── index.html        # Flask 웹 인터페이스
├── requirements.txt      # Python 패키지 목록
├── Procfile             # 배포 설정
├── runtime.txt          # Python 버전
├── setup.sh             # 설치 스크립트
└── README.md            # 프로젝트 설명
```

## 🌐 배포

### Streamlit Cloud
1. GitHub에 코드 업로드
2. https://share.streamlit.io 에서 배포

### Heroku
```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

### Docker
```bash
docker build -t pdf-ocr .
docker run -p 8501:8501 pdf-ocr
```

## 📝 라이선스

MIT License

## 🤝 기여

이슈나 풀 리퀘스트를 환영합니다!

## 📞 문의

문제가 있으시면 이슈를 생성해주세요.
