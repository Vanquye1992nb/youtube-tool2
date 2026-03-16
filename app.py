import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN 5 ẢNH ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    /* Nền màu Slate chuẩn ảnh gốc 843 */
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Hiện rõ tiêu đề các ô nhập liệu (Fix lỗi mất tiêu đề) */
    label, .stMarkdown p { 
        color: #ffffff !important; 
        font-weight: 500 !important; 
        display: block !important;
        opacity: 1 !important;
    }

    .card { 
        background-color: #363d4a; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 20px;
    }

    .title-gold { color: #f1c40f; font-size: 28px; font-weight: bold; text-align: center; }
    
    /* Nút bấm Tạo nội dung */
    .stButton>button { 
        background-color: #2563eb !important; 
        color: white !important; 
        border-radius: 8px;
        width: 100%;
    }
    
    /* Thẻ tag bong bóng ảnh 846 */
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 5px 12px; 
        border-radius: 20px; display: inline-block; margin: 4px; border: 1px solid #718096;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO AI VỚI FIX 404 ---
def get_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # Bỏ qua v1beta, sử dụng model định danh chuẩn nhất
        return genai.GenerativeModel('gemini-1.5-flash-001')
    except Exception as e:
        return None

if 'step' not in st.session_state: st.session_state.step = 1
if 'seo_data' not in st.session_state: st.session_state.seo_data = {}

with st.sidebar:
    st.header("Cấu hình")
    api_key = st.text_input("Gemini API Key:", type="password")

# --- GIAO DIỆN NHẬP LIỆU (Ảnh 843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            ref = st.text_input("Link video đối thủ (Tùy chọn)", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", key="kw")
            chan = st.text_input("Link kênh của bạn", key="chan")
        
        if st.button("🚀 Tạo Nội Dung Tối Ưu"):
            if kw and api_key:
                model = get_model(api_key)
                with st.spinner("Đang xử lý..."):
                    try:
                        prompt = f"SEO Youtube cho từ khóa '{kw}'. Trả về JSON: 'titles' (10 cái), 'tags' (25 cái), 'desc', 'comment'."
                        res = model.generate_content(prompt)
                        # Fix lỗi bóc tách JSON
                        clean_text = re.search(r'\{.*\}', res.text, re.DOTALL).group()
                        st.session_state.seo_data = json.loads(clean_text)
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi: {str(e)}. Hãy thử lại hoặc kiểm tra Key.")
            else: st.warning("Điền Từ khóa & Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- GIAO DIỆN KẾT QUẢ (Ảnh 844, 845, 846) ---
if st.session_state.step >= 2:
    st.write(f"### KẾT QUẢ CHO: {st.session_state.current_kw}")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ HẤP DẪN**")
    for t in st.session_state.seo_data.get('titles', []):
        st.write(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 TỪ KHÓA TÌM KIẾM CAO**")
    tags = "".join([f'<span class="tag-chip">{tag}</span>' for tag in st.session_state.seo_data.get('tags', [])])
    st.markdown(tags, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 Làm lại"):
        st.session_state.step = 1
        st.rerun()
