#!/bin/bash
# Tesseract OCR 설치
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng
sudo apt-get install -y poppler-utils

# Python 패키지 설치
pip install -r requirements.txt
