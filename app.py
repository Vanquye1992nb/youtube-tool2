import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (Tone màu Slate & Blue - Sáng và Dịu mắt) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    /* Nền chính sáng hơn, không bị đen kịt */
    .stApp { background-color: #f0f2f6; color: #1e293b; }
    
    /* Card chứa nội dung */
    .card { 
        background-color: #ffffff; 
        padding: 30px; 
        border-radius: 16px; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 1px solid #e2e8f0;
    }

    /* Tiêu đề chính */
    .title-main { 
        color: #1e3a8a; 
        font-size: 32px; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 5px;
    }
    .subtitle { color: #64748b; text-align: center; margin-bottom: 30px; }

    /* Label của các ô nhập liệu */
    label { color: #334155 !important; font-weight: 600 !important; font-size: 15px !important; }

    /* Nút bấm Blue Royal */
    .stButton>button { 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold; 
        width: 100%; 
        background: #2563eb !important;
        color: white !important;
        border: none;
    }
    
    /* Nút phân tích ngang */
    .btn-tool>div>button {
        background-color: #f8fafc !important;
        color: #2563eb !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* Thẻ Tag chuẩn mẫu */
    .tag-chip { 
        background-color: #e2e8f0; 
        color: #1e40af; 
        padding: 6px 14px; 
        border-radius: 20px; 
        display: inline-block; 
        margin: 5px; 
        font-size: 13px;
        border: 1px solid #cbd5e1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- QUẢN LÝ SESSION ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'seo_data' not in st.session_state: st.session_state.seo_data = {}

with st.sidebar:
    st.header("⚙️ Cấu hình Hệ thống")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    st.divider()
    if st.button("🔄 Làm mới quy trình"):
        st.session_state.step = 1
        st.session_state.seo_data = {}
        st.rerun()

def call_gemini(prompt):
    try:
        # Sửa lỗi 404 bằng cách gọi đúng model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi kết nối AI: {str(e)}")
        return None

# ---------------------------------------------------------
# BƯỚC 1: FORM NHẬP LIỆU (Giống Ảnh 1000000843)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown('<p class="title-main">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Đưa video của bạn lên top tìm kiếm YouTube!</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"])
            link_ref = st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link tại đây...")
        with col2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: Cách làm bánh rán")
            link_chan = st.text_input("Link kênh của bạn (Tùy chọn)")
        
        if st.button("Tạo Nội Dung Tối Ưu"):
            if kw and api_key:
                with st.spinner("Đang phân tích dữ liệu..."):
                    prompt = f"""
                    Nhiệm vụ: Phân tích SEO Youtube cho từ khóa '{kw}'.
                    Hãy trả về 1 chuỗi JSON duy nhất (không có markdown) gồm:
                    'titles': [10 tiêu đề hay nhất],
                    'tags': [25 từ khóa tìm kiếm cao],
                    'description': 'Mô tả video chuẩn SEO dài',
                    'trend': 'Dự đoán xu hướng hot hay không',
                    'comment': 'Bình luận ghim hay',
                    'category': 'Danh mục đề xuất'
                    """
                    res = call_gemini(prompt)
                    if res:
                        try:
                            # Làm sạch text để lấy JSON
                            clean_json = re.search(r'\{.*\}', res, re.DOTALL).group()
                            st.session_state.seo_data = json.loads(clean_json)
                            st.session_state.kw = kw
                            st.session_state.step = 2
                            st.rerun()
                        except:
                            st.error("Lỗi xử lý dữ liệu từ AI. Hãy thử lại!")
            else: st.warning("Vui lòng điền Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 2: DASHBOARD KẾT QUẢ (Giống Ảnh 1000000844/846)
# ---------------------------------------------------------
if st.session_state.step >= 2:
    st.markdown(f"### 📈 KẾT QUẢ TỐI ƯU CHO: {st.session_state.kw.upper()}")
    
    # Trend Predictor
    st.info(f"🔥 **Xu hướng:** {st.session_state.seo_data.get('trend')}")

    # Công cụ phân tích ngang
    st.write("🚀 **CÔNG CỤ PHÂN TÍCH ĐỐI THỦ:**")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("🔵 Danh mục video", key="c1")
    with c2: st.button("🟢 Thẻ tag video", key="c2")
    with c3: st.button("🟣 Thông tin video", key="c3")

    # 10 Tiêu đề
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for i, t in enumerate(st.session_state.seo_data.get('titles', [])):
        st.markdown(f"<div style='background:#f1f5f9; padding:8px; border-radius:8px; margin-bottom:6px; color:#1e293b;'><b>{i+1}.</b> {t}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 25 Tags & Mô tả
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("📊 **25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO**")
    tag_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in st.session_state.seo_data.get('tags', [])])
    st.markdown(tag_html, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("📝 **MÔ TẢ CHUẨN SEO**")
    st.text_area("Copy mô tả:", st.session_state.seo_data.get('description'), height=150)
    
    st.markdown("💬 **BÌNH LUẬN GIM**")
    st.success(st.session_state.seo_data.get('comment'))

    if st.button("🎨 Tiếp theo: Tạo Thumbnail Prompt"):
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 3: THUMBNAIL (Ảnh 1000000847)
# ---------------------------------------------------------
if st.session_state.step >= 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🎨 **CÔNG CỤ TẠO ẢNH MINH HỌA**")
    text_img = st.text_input("Văn bản trên Thumbnail", value="BÍ MẬT SEO")
    style = st.select_slider("Chọn phong cách", options=["Ảnh Thật", "3D Render", "Điện Ảnh", "Hoạt Hình"])
    
    if st.button("Tạo Prompt Ảnh"):
        prompt = f"YouTube thumbnail for '{st.session_state.kw}', text '{text_img}', style {style}, 8k, vibrant colors."
        st.code(prompt)
    
    st.divider()
    if st.button("🔄 Tạo nội dung mới"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
