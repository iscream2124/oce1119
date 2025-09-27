#!/usr/bin/env python3
"""
PDF OCR 스크립트
PDF 파일을 이미지로 변환하고 OCR을 수행합니다.
"""

import os
import sys
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
import argparse

def pdf_to_text(pdf_path, output_dir, lang='kor+eng'):
    """
    PDF 파일을 텍스트로 변환합니다.
    
    Args:
        pdf_path (str): PDF 파일 경로
        output_dir (str): 출력 디렉토리
        lang (str): OCR 언어 설정
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    
    # 출력 디렉토리 생성
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"PDF 파일 처리 중: {pdf_path}")
    print(f"출력 디렉토리: {output_dir}")
    
    try:
        # PDF를 이미지로 변환
        print("PDF를 이미지로 변환 중...")
        images = convert_from_path(pdf_path, dpi=300)
        
        all_text = []
        
        for i, image in enumerate(images):
            print(f"페이지 {i+1}/{len(images)} OCR 처리 중...")
            
            # OCR 수행
            text = pytesseract.image_to_string(image, lang=lang)
            
            # 페이지별 텍스트 저장
            page_text_file = output_dir / f"page_{i+1:03d}.txt"
            with open(page_text_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            all_text.append(f"=== 페이지 {i+1} ===\n{text}\n")
            
            print(f"페이지 {i+1} 완료")
        
        # 전체 텍스트 저장
        full_text_file = output_dir / "full_text.txt"
        with open(full_text_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))
        
        print(f"OCR 완료! 결과가 {output_dir}에 저장되었습니다.")
        print(f"- 전체 텍스트: {full_text_file}")
        print(f"- 페이지별 텍스트: page_*.txt")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='PDF OCR 도구')
    parser.add_argument('pdf_path', help='PDF 파일 경로')
    parser.add_argument('output_dir', help='출력 디렉토리')
    parser.add_argument('--lang', default='kor+eng', help='OCR 언어 (기본값: kor+eng)')
    
    args = parser.parse_args()
    
    if not Path(args.pdf_path).exists():
        print(f"PDF 파일을 찾을 수 없습니다: {args.pdf_path}")
        sys.exit(1)
    
    success = pdf_to_text(args.pdf_path, args.output_dir, args.lang)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
