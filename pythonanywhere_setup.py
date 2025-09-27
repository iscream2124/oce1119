#!/usr/bin/env python3
"""
PythonAnywhere 배포용 설정 스크립트
"""

import os
import subprocess

def setup_pythonanywhere():
    """PythonAnywhere 환경 설정"""
    
    # 필요한 패키지 설치
    packages = [
        'streamlit',
        'pytesseract', 
        'pdf2image',
        'pillow'
    ]
    
    for package in packages:
        try:
            subprocess.run(['pip3.10', 'install', '--user', package], check=True)
            print(f"✅ {package} 설치 완료")
        except subprocess.CalledProcessError:
            print(f"❌ {package} 설치 실패")
    
    print("PythonAnywhere 설정 완료!")
    print("웹 앱에서 다음 명령어로 실행하세요:")
    print("streamlit run app.py --server.port 8080 --server.address 0.0.0.0")

if __name__ == "__main__":
    setup_pythonanywhere()
