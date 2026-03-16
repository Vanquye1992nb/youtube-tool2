import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN 5 ẢNH (ẢNH 843-847) ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube ", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Hiện tiêu đề trắng rõ (Fix lỗi ảnh 860) */
    label, .stMarkdown p { 
        color: #ffffff !important; 
        font-weight: 600 !important;
        display: block !important;
    }

    .card { 
        background-color: #363d4a; padding: 25px; 
        border-radius: 15px; border: 1px solid #4a5568; margin-bottom: 20px;
    }

    .title-gold { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #bdc3c7; text-align: center; margin-bottom: 25px; font-size: 14px; }

    /* Nút Tạo Nội Dung (Ảnh 843) */
    .stButton>button { 
        background: #2563eb !important; color: white !important; 
        border-radius: 8px; height: 3.5em; font-weight: bold; width: 100%; border: none;
    }

    /* Các nút chức năng (Ảnh 844) */
    .btn-blue button { background-color: #1e40af !important; color: white !important; }
    .btn-green button { background-color: #166534 !important; color: white !important; }
    .btn-purple button { background-color: #6b21a8 !important; color: white !important; }

    /* Tag bong bóng (Ảnh 846) */
    .tag-chip { 
        background: #4a5568; color: #e2e8f0; padding: 6px 14px; 
        border-radius: 20px; display: inline-block; margin: 4px; border: 1px solid #718096; font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC AI THÔNG MINH (FIX 404 & FIX KHÔNG RA TIN) ---
def get_seo_content(api_key, keyword):
    try:
        genai.configure(api_key=api_key)
        
        # Thử lần lượt các model để tránh lỗi 404 (Ảnh 859)
        models_to_try = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
        model = None
        
        for m_name in models_to_try:
            try:
                model = genai.GenerativeModel(m_name)
                # Test thử 1 câu ngắn xem có 404 không
                model.generate_content("test")
                break 
            except:
                continue
        
        if not model:
            return "ERROR_404"

        prompt = f"""
        Bạn là chuyên gia SEO Youtube. Hãy phân tích từ khóa '{keyword}'.
        Trả về DUY NHẤT mã JSON theo cấu trúc này (không viết gì thêm):
        {{
            "titles": ["10 tiêu đề hấp dẫn nhất"],
            "tags": ["25 thẻ tag hot nhất"],
            "desc": "Mô tả chuẩn SEO dài, có hashtag",
            "comment": "Bình luận ghim kêu gọi hành động",
            "category": "Giáo dục / Công nghệ"
        }}
        """
        response = model.generate_content(prompt)
        
        # Bóc tách JSON an toàn (Fix lỗi không ra tin)
        json_str = re.search(r'\{.*\}', response.text, re.DOTALL).group()
        return json.loads(json_str)
    except Exception as e:
        return str(e)

# Quản lý Session
if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ Cấu hình API")
    api_key = st.text_input("Gemini API Key:", type="password")
    if st.button("🔄 Làm mới Tool"):
        st.session_state.clear()
        st.rerun()

# --- BƯỚC 1: FORM NHẬP LIỆU (ẢNH 843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Đưa video của bạn lên top tìm kiếm YouTube!</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            st.text_input("Link video đối thủ (Tùy chọn)", key="ref", placeholder="Dán link...")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", key="kw", placeholder="Ví dụ: Cách làm giàu")
            st.text_input("Link kênh YouTube của bạn (Tùy chọn)", key="chan")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                with st.spinner("Đang tra cứu dữ liệu..."):
                    res = get_seo_content(api_key, kw)
                    if res == "ERROR_404":
                        st.error("Lỗi 404: Không tìm thấy Model. Hãy thử lại sau vài phút hoặc đổi API Key.")
                    elif isinstance(res, dict):
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error(f"Lỗi: {res}")
            else: st.warning("Vui lòng nhập Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ (ẢNH 844, 845, 846, 847) ---
if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ CHO: <span style='color:#f1c40f'>{st.session_state.current_kw.upper()}</span>", unsafe_allow_html=True)
    
    # Các nút công cụ (Ảnh 844)
    st.write("🚀 CÔNG CỤ PHÂN TÍCH:")
    bc1, bc2, bc3 = st.columns(3)
    with bc1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button(f"📁 {st.session_state.data.get('category')}"); st.markdown('</div>', unsafe_allow_html=True)
    with bc2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("✅ Đã tạo 25 Tags"); st.markdown('</div>', unsafe_allow_html=True)
    with bc3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("ℹ️ Thông tin Video"); st.markdown('</div>', unsafe_allow_html=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for t in st.session_state.data.get('titles', []):
        st.write(f"🔹 {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 25 Tags (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📈 **25 TỪ KHÓA TÌM KIẾM CAO**")
    tags_html = "".join([f'<span class="tag-chip">#{tag}</span>' for tag in st.session_state.data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    # Thumbnail Prompt (Ảnh 847)
    st.divider()
    st.write("🎨 **PROMPT TẠO THUMBNAIL:**")
    st.code(f"YouTube thumbnail for '{st.session_state.current_kw}', bold text, high contrast, 4k.")
    
    if st.button("🔄 Tạo nội dung mới"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
