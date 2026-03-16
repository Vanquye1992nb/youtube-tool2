import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN (Ảnh 843, 844) ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    /* Nền Slate chuẩn ảnh 843 */
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Ép hiển thị tiêu đề các ô nhập liệu trắng rõ */
    label, .stMarkdown p { 
        color: #ffffff !important; 
        font-weight: 500 !important; 
        display: block !important;
    }

    .card { 
        background-color: #363d4a; 
        padding: 25px; 
        border-radius: 15px; 
        margin-bottom: 20px;
        border: 1px solid #4a5568;
    }

    .title-gold { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; }
    
    /* Nút Tạo Nội Dung Xanh (Ảnh 843) */
    .stButton>button { 
        background-color: #2563eb !important; 
        color: white !important; 
        border-radius: 10px;
        height: 3.5em;
        width: 100%;
        border: none;
    }
    
    /* Thẻ Tag (Ảnh 846) */
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 6px 14px; 
        border-radius: 20px; display: inline-block; margin: 4px; border: 1px solid #718096;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FIX LỖI 404 BẰNG MODEL NAME CHUẨN ---
def get_ai_response(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng model_name đầy đủ để tránh lỗi 404 trên Streamlit Cloud
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi API: {str(e)}")
        return None

if 'step' not in st.session_state: st.session_state.step = 1
if 'seo_results' not in st.session_state: st.session_state.seo_results = {}

with st.sidebar:
    st.header("🔑 Cấu hình")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")

# --- BƯỚC 1: NHẬP LIỆU ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            ref_link = st.text_input("Link video đối thủ (Tùy chọn)", key="ref")
        with col2:
            keyword = st.text_input("Từ khóa chính (Bắt buộc)", key="kw")
            channel = st.text_input("Link kênh YouTube của bạn (Tùy chọn)", key="chan")
        
        if st.button("🚀 Tạo Nội Dung Tối Ưu"):
            if keyword and api_key:
                with st.spinner("Đang phân tích..."):
                    prompt = f"Phân tích SEO Youtube cho '{keyword}'. Trả về JSON: 'titles' (10 cái), 'tags' (25 cái), 'desc', 'comment'."
                    raw_res = get_ai_response(api_key, prompt)
                    if raw_res:
                        try:
                            clean_json = re.search(r'\{.*\}', raw_res, re.DOTALL).group()
                            st.session_state.seo_results = json.loads(clean_json)
                            st.session_state.current_kw = keyword
                            st.session_state.step = 2
                            st.rerun()
                        except:
                            st.error("Không thể xử lý dữ liệu AI. Hãy thử lại.")
            else: st.warning("Hãy điền Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ (Ảnh 844, 846) ---
if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ TỐI ƯU: {st.session_state.current_kw.upper()}")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for i, t in enumerate(st.session_state.seo_results.get('titles', [])):
        st.info(f"Tiêu đề {i+1}: {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📈 **25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO**")
    all_tags = "".join([f'<span class="tag-chip">#{t}</span>' for t in st.session_state.seo_results.get('tags', [])])
    st.markdown(all_tags, unsafe_allow_html=True)
    
    if st.button("🔄 Làm Video Mới"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
