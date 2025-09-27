#!/usr/bin/env python3
"""
간단한 웹 OCR 인터페이스 (Flask 기반)
"""

from flask import Flask, request, render_template, jsonify, send_file
import os
import tempfile
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
import zipfile
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def pdf_to_text(pdf_path, lang='kor+eng'):
    """PDF를 텍스트로 변환"""
    try:
        images = convert_from_path(pdf_path, dpi=300)
        all_text = []
        page_texts = []
        
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=lang)
            page_texts.append(f"=== 페이지 {i+1} ===\n{text}\n")
            all_text.append(text)
        
        return '\n'.join(page_texts), all_text, len(images)
    except Exception as e:
        return None, None, 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 선택되지 않았습니다.'})
    
    file = request.files['file']
    lang = request.form.get('lang', 'kor+eng')
    
    if file.filename == '':
        return jsonify({'error': '파일이 선택되지 않았습니다.'})
    
    if file and file.filename.lower().endswith('.pdf'):
        try:
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                file.save(tmp_file.name)
                tmp_path = tmp_file.name
            
            # OCR 처리
            full_text, page_texts, num_pages = pdf_to_text(tmp_path, lang)
            
            # 임시 파일 삭제
            os.unlink(tmp_path)
            
            if full_text is not None:
                return jsonify({
                    'success': True,
                    'full_text': full_text,
                    'page_texts': page_texts,
                    'num_pages': num_pages,
                    'filename': file.filename
                })
            else:
                return jsonify({'error': 'OCR 처리 중 오류가 발생했습니다.'})
                
        except Exception as e:
            return jsonify({'error': f'처리 중 오류가 발생했습니다: {str(e)}'})
    
    return jsonify({'error': 'PDF 파일만 업로드 가능합니다.'})

@app.route('/download/<filename>')
def download_file(filename):
    # 다운로드 로직 (필요시 구현)
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
