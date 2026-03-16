import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Gemini 3", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    label { color: #ffffff !important; font-weight: bold !important; }
    .card { background-color: #363d4a; padding: 20px; border-radius: 12px; border: 1px solid #4a5568; margin-bottom: 20px; }
    .title-gold { color: #f1c40f; font-size: 28px; font-weight: 800; text-align: center; }
    .stButton>button { background-color: #2563eb !important; color: white !important; width: 100%; border-radius: 8px; font-weight: bold; }
    .tag-chip { background-color: #4a5568; color: #e2e8f0; padding: 5px 12px; border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #718096; }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM GỌI GEMINI 3 FLASH (MỚI NHẤT 2026) ---
def call_gemini_3(api_key, keyword):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng Gemini 3 Flash theo cập nhật tháng 3/2026
        model = genai.GenerativeModel('gemini-3-flash')
        
        prompt = f"Phân tích Youtube '{keyword}'. Trả về JSON: 'titles' (10), 'tags' (25), 'desc'."
        response = model.generate_content(prompt)
        
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        return str(e)

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Gemini API Key:", type="password")

if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video v3.0</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: Cách làm giàu")
        if st.button("🚀 TẠO NỘI DUNG VỚI GEMINI 3"):
            if kw and api_key:
                with st.spinner("Đang sử dụng Gemini 3 Flash..."):
                    res = call_gemini_3(api_key, kw)
                    if isinstance(res, dict):
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    else: st.error(f"Lỗi API: {res}")
            else: st.warning("Vui lòng điền đủ thông tin!")
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ: {st.session_state.current_kw.upper()}")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ ĐỀ XUẤT (GEMINI 3)**")
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
