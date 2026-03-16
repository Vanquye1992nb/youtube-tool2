import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (CHÍNH XÁC THEO 5 ẢNH GỐC) ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    /* Nền tối sâu sang trọng */
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Card chứa nội dung */
    .card { 
        background-color: #363d4a; 
        padding: 30px; 
        border-radius: 15px; 
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 25px;
    }

    /* Tiêu đề Chuyên Gia SEO Video (Màu vàng gold) */
    .title-gold { 
        color: #f1c40f; 
        font-size: 30px; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 5px;
    }
    .subtitle { color: #bdc3c7; text-align: center; margin-bottom: 30px; font-size: 14px; }

    /* Hiển thị rõ tiêu đề các ô nhập liệu */
    label { color: #ffffff !important; font-weight: 500 !important; margin-bottom: 10px !important; display: block !important; }

    /* Nút bấm Tạo Nội Dung (Xanh dương) */
    .stButton>button { 
        border-radius: 8px; 
        height: 3.5em; 
        font-weight: bold; 
        width: 100%; 
        background-color: #2563eb !important;
        color: white !important;
        border: none;
    }

    /* Thẻ Tag bong bóng (Xám xanh) */
    .tag-chip { 
        background-color: #4a5568; 
        color: #e2e8f0; 
        padding: 6px 14px; 
        border-radius: 20px; 
        display: inline-block; 
        margin: 5px; 
        font-size: 13px;
        border: 1px solid #718096;
    }

    /* Nút chức năng Phân tích (Xanh dương, Xanh lá, Tím) */
    .btn-blue>div>button { background-color: #1e3a8a !important; color: white !important; }
    .btn-green>div>button { background-color: #166534 !important; color: white !important; }
    .btn-purple>div>button { background-color: #6b21a8 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- QUẢN LÝ SESSION ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'seo_data' not in st.session_state: st.session_state.seo_data = {}

with st.sidebar:
    st.header("⚙️ Cấu hình API")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    if st.button("🔄 Làm mới quy trình"):
        st.session_state.clear()
        st.rerun()

def safe_generate(prompt):
    try:
        # Sử dụng model_name ổn định nhất để tránh lỗi 404
        model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi API: {str(e)}")
        return None

# ---------------------------------------------------------
# BƯỚC 1: FORM NHẬP LIỆU (Ảnh 1000000843)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Đưa video của bạn lên top tìm kiếm YouTube!</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link tại đây...", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="ví dụ: cách làm bánh flan", key="kw_input")
            st.text_input("Link kênh YouTube của bạn (Tùy chọn)", key="chan")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Tạo Nội Dung Tối Ưu"):
            if kw and api_key:
                with st.spinner("Đang phân tích xu hướng và nội dung..."):
                    prompt = f"Phân tích SEO Youtube '{kw}'. Trả về JSON: 'trend' (phân tích volume/hot), 'titles' (10 cái), 'tags' (25 cái), 'desc', 'comment'."
                    res = safe_generate(prompt)
                    if res:
                        match = re.search(r'\{.*\}', res, re.DOTALL)
                        if match:
                            st.session_state.seo_data = json.loads(match.group())
                            st.session_state.current_kw = kw
                            st.session_state.step = 2
                            st.rerun()
            else: st.warning("Vui lòng điền đủ Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 2: KẾT QUẢ & TREND PREDICTOR (Ảnh 1000000844/846)
# ---------------------------------------------------------
if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ TỐI ƯU CHO TỪ KHÓA: <span style='color:#f1c40f'>{st.session_state.current_kw.upper()}</span>", unsafe_allow_html=True)
    
    # Trend Predictor
    st.markdown(f'<div style="background:#1e293b; padding:15px; border-radius:10px; border-left:5px solid #f1c40f; margin-bottom:20px;">🔥 <b>DỰ ĐOÁN XU HƯỚNG:</b> {st.session_state.seo_data.get("trend")}</div>', unsafe_allow_html=True)

    # Nút công cụ phân tích (Màu sắc chuẩn ảnh 844)
    st.write("🚀 CÔNG CỤ PHÂN TÍCH ĐỐI THỦ:")
    bc1, bc2, bc3 = st.columns(3)
    with bc1: st.markdown('<div class="btn-blue">', unsafe_allow_html=True); st.button("Kiểm tra danh mục video"); st.markdown('</div>', unsafe_allow_html=True)
    with bc2: st.markdown('<div class="btn-green">', unsafe_allow_html=True); st.button("Kiểm tra thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with bc3: st.markdown('<div class="btn-purple">', unsafe_allow_html=True); st.button("Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for i, t in enumerate(st.session_state.seo_data.get('titles', [])):
        st.markdown(f"<div style='background:#2d3748; padding:10px; border-radius:8px; margin-bottom:8px; border-left:3px solid #f1c40f;'><b>Tiêu đề {i+1}:</b> {t}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Thẻ Tag & Mô tả (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📈 **25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO**")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in st.session_state.seo_data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.divider()
    st.text_area("📝 Mô tả chuẩn SEO:", st.session_state.seo_data.get('desc'), height=150)
    st.info(f"💬 Bình luận ghim: {st.session_state.seo_data.get('comment')}")
    
    if st.button("🎨 Tiếp theo: Tạo Thumbnail Prompt"):
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 3: THUMBNAIL (Ảnh 1000000847)
# ---------------------------------------------------------
if st.session_state.step >= 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🎨 **CÔNG CỤ TẠO ẢNH MINH HỌA**")
    txt_thumb = st.text_input("Văn bản trên Thumbnail", value="BÍ MẬT SEO")
    st.write("Chọn phong cách:")
    st.columns(5)[0].button("Ảnh Thật") # Giả lập giao diện chọn nhanh
    
    if st.button("Tạo Prompt Ảnh"):
        st.code(f"High-quality YouTube thumbnail for '{st.session_state.current_kw}', text '{txt_thumb}', cinematic lighting, 8k.")
    
    st.divider()
    c_dl, c_new = st.columns(2)
    with c_dl: st.button("📥 Tải về toàn bộ", type="secondary")
    with c_new: 
        if st.button("🔄 Tạo nội dung mới"):
            st.session_state.step = 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
