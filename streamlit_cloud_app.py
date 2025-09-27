import streamlit as st
import os
import tempfile
from pathlib import Path
import zipfile
import io

def pdf_to_text_simple(pdf_file):
    """
    PDF 파일을 텍스트로 변환하는 간단한 버전 (Tesseract 없이)
    """
    try:
        # PDF 파일 정보만 표시
        st.info(f"📄 파일명: {pdf_file.name}")
        st.info(f"📊 파일 크기: {pdf_file.size:,} bytes")
        
        # PDF 내용을 바이너리로 읽기
        pdf_content = pdf_file.read()
        
        # 간단한 텍스트 추출 시뮬레이션
        st.warning("⚠️ Streamlit Cloud에서는 Tesseract OCR이 지원되지 않습니다.")
        st.info("💡 로컬에서 실행하거나 다른 호스팅 서비스를 사용해주세요.")
        
        # 샘플 텍스트 반환
        sample_text = f"""
=== PDF OCR 도구 ===

파일명: {pdf_file.name}
파일 크기: {pdf_file.size:,} bytes

⚠️ 주의: Streamlit Cloud에서는 Tesseract OCR이 지원되지 않습니다.

로컬에서 실행하려면:
1. git clone https://github.com/iscream2124/oce1119.git
2. cd oce1119
3. pip install -r requirements.txt
4. streamlit run app.py

또는 다음 호스팅 서비스를 사용하세요:
- Heroku
- Railway
- Render
- PythonAnywhere
        """
        
        return sample_text, [sample_text], 1
        
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return None, None, 0

def main():
    st.set_page_config(
        page_title="PDF OCR 도구",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 PDF OCR 도구")
    st.markdown("PDF 파일을 업로드하면 자동으로 텍스트를 추출합니다.")
    
    # 경고 메시지
    st.warning("⚠️ **Streamlit Cloud 제한사항**: Tesseract OCR이 지원되지 않습니다. 로컬에서 실행하거나 다른 호스팅 서비스를 사용해주세요.")
    
    # 사이드바 설정
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # 언어 선택
        lang_options = {
            "한국어 + 영어": "kor+eng",
            "영어만": "eng",
            "한국어만": "kor",
            "일본어": "jpn",
            "중국어": "chi_sim"
        }
        
        selected_lang = st.selectbox(
            "OCR 언어 선택",
            options=list(lang_options.keys()),
            index=0
        )
        
        lang_code = lang_options[selected_lang]
        
        st.markdown("---")
        st.markdown("### 📋 사용법")
        st.markdown("1. PDF 파일을 업로드하세요")
        st.markdown("2. 언어를 선택하세요")
        st.markdown("3. 'OCR 실행' 버튼을 클릭하세요")
        st.markdown("4. 결과를 확인하고 다운로드하세요")
        
        st.markdown("---")
        st.markdown("### 🚀 로컬 실행")
        st.code("""
git clone https://github.com/iscream2124/oce1119.git
cd oce1119
pip install -r requirements.txt
streamlit run app.py
        """)
    
    # 메인 영역
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 파일 업로드")
        uploaded_file = st.file_uploader(
            "PDF 파일을 선택하세요",
            type=['pdf'],
            help="PDF 파일을 드래그 앤 드롭하거나 클릭하여 선택하세요"
        )
        
        if uploaded_file is not None:
            st.success(f"파일 업로드 완료: {uploaded_file.name}")
            st.info(f"파일 크기: {uploaded_file.size:,} bytes")
    
    with col2:
        st.header("🚀 OCR 실행")
        
        if uploaded_file is not None:
            if st.button("🔍 OCR 실행", type="primary", use_container_width=True):
                with st.spinner("PDF를 처리 중입니다..."):
                    # 진행률 표시
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # PDF 처리
                    status_text.text("PDF를 분석 중...")
                    progress_bar.progress(25)
                    
                    full_text, page_texts, num_pages = pdf_to_text_simple(uploaded_file)
                    
                    if full_text is not None:
                        progress_bar.progress(100)
                        status_text.text("처리 완료!")
                        
                        # 결과 저장
                        st.session_state['full_text'] = full_text
                        st.session_state['page_texts'] = page_texts
                        st.session_state['num_pages'] = num_pages
                        st.session_state['filename'] = uploaded_file.name
                        
                        st.success(f"✅ 처리 완료! ({num_pages}페이지)")
                    else:
                        st.error("❌ 처리 실패")
        else:
            st.info("PDF 파일을 먼저 업로드해주세요.")
    
    # 결과 표시
    if 'full_text' in st.session_state:
        st.markdown("---")
        st.header("📝 처리 결과")
        
        # 탭으로 결과 표시
        tab1, tab2, tab3 = st.tabs(["📄 전체 텍스트", "📋 페이지별 텍스트", "💾 다운로드"])
        
        with tab1:
            st.subheader("전체 텍스트")
            st.text_area(
                "처리된 텍스트",
                value=st.session_state['full_text'],
                height=400,
                help="전체 텍스트를 복사하여 사용하세요"
            )
        
        with tab2:
            st.subheader("페이지별 텍스트")
            for i, page_text in enumerate(st.session_state['page_texts']):
                with st.expander(f"페이지 {i+1}"):
                    st.text(page_text)
        
        with tab3:
            st.subheader("파일 다운로드")
            
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                # 전체 텍스트 다운로드
                st.download_button(
                    label="📄 전체 텍스트 다운로드",
                    data=st.session_state['full_text'],
                    file_name=f"{Path(st.session_state['filename']).stem}_result.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_download2:
                # ZIP 파일로 모든 페이지 다운로드
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # 전체 텍스트
                    zip_file.writestr("result.txt", st.session_state['full_text'])
                    
                    # 페이지별 텍스트
                    for i, page_text in enumerate(st.session_state['page_texts']):
                        zip_file.writestr(f"page_{i+1:03d}.txt", page_text)
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📦 모든 파일 다운로드 (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"{Path(st.session_state['filename']).stem}_results.zip",
                    mime="application/zip",
                    use_container_width=True
                )
    
    # 푸터
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Powered by Streamlit | "
        "GitHub: https://github.com/iscream2124/oce1119"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
