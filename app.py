import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (CHUẨN 5 ẢNH) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    label, .stMarkdown p { color: #ffffff !important; font-weight: bold !important; display: block !important; }
    .card { background-color: #363d4a; padding: 25px; border-radius: 12px; border: 1px solid #4a5568; margin-bottom: 20px; }
    .title-gold { color: #f1c40f; font-size: 28px; font-weight: 800; text-align: center; }
    .stButton>button { background-color: #2563eb !important; color: white !important; width: 100%; border-radius: 8px; font-weight: bold; }
    .tag-chip { background-color: #4a5568; color: #e2e8f0; padding: 5px 12px; border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #718096; }
    </style>
    """, unsafe_allow_html=True)

def call_ai_fix_404(api_key, keyword):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng định danh đầy đủ để tránh lỗi 404
        model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')
        
        prompt = f"Phân tích SEO Youtube cho '{keyword}'. Trả về JSON: 'titles' (10), 'tags' (25), 'desc'."
        response = model.generate_content(prompt)
        
        # Bóc tách JSON
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        return str(e)

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập API Key:", type="password")

if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Ngôn ngữ", ["Tiếng Việt"], key="lang")
            st.text_input("Link video đối thủ", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính", key="kw")
            st.text_input("Link kênh của bạn", key="chan")
        
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                with st.spinner("Đang xử lý..."):
                    res = call_ai_fix_404(api_key, kw)
                    if isinstance(res, dict):
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    else: st.error(f"Lỗi: {res}")
            else: st.warning("Vui lòng điền đủ Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ: {st.session_state.current_kw.upper()}")
    
    # Hiển thị kết quả đúng như ảnh mẫu 861
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ HẤP DẪN**")
    for t in st.session_state.data.get('titles', []):
        st.write(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 THẺ TAGS SEO**")
    tags = "".join([f'<span class="tag-chip">{t}</span>' for t in st.session_state.data.get('tags', [])])
    st.markdown(tags, unsafe_allow_html=True)
    
    if st.button("🔄 Tạo từ khóa khác"):
        st.session_state.step = 1
        st.rerun()
