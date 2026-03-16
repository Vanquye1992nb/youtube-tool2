import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN CHUẨN PREMIUM ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube ", layout="centered")

st.markdown("""
    <style>
    /* Tổng thể nền tối sâu */
    .main { background-color: #0f111a; color: #e1e1e6; }
    .stApp { background-color: #0f111a; }
    
    /* Card chứa nội dung */
    .card { 
        background-color: #1a1c26; 
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid #2d2f3d; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 25px;
    }

    /* Tiêu đề Gold chuẩn mẫu */
    .title-gold { 
        color: #f1c40f; 
        font-size: 32px; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .subtitle { color: #8b949e; text-align: center; margin-bottom: 30px; font-size: 14px; }

    /* Button phong cách hiện đại */
    .stButton>button { 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold; 
        width: 100%; 
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        border: none;
    }
    .btn-main { background: linear-gradient(135deg, #3498db, #2980b9) !important; color: white !important; }
    .btn-main:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(52,152,219,0.4); }

    /* Tags chuẩn như ảnh mẫu 846 */
    .tag-chip { 
        background-color: #2d2f3d; 
        color: #adbac7; 
        padding: 6px 16px; 
        border-radius: 25px; 
        display: inline-block; 
        margin: 5px; 
        border: 1px solid #444c56; 
        font-size: 13px;
    }

    /* Input & Selectbox decor */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #222533 !important;
        border: 1px solid #3d444d !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    /* Trend Predictor Badge */
    .metric-card {
        background: #222533;
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #f1c40f;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- QUẢN LÝ SESSION ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

# --- CẤU HÌNH API TRONG SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", width=60)
    st.subheader("Hệ thống AI")
    api_key = st.text_input("Gemini API Key:", type="password")
    if api_key: 
        genai.configure(api_key=api_key)
    st.divider()
    if st.button("🔄 Làm mới toàn bộ"):
        st.session_state.step = 1
        st.session_state.data = {}
        st.rerun()

# ---------------------------------------------------------
# BƯỚC 1: FORM NHẬP LIỆU (Giống Ảnh 1000000843 & 850)
# ---------------------------------------------------------
if st.session_state.step >= 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Đưa video của bạn lên top tìm kiếm YouTube!</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English", "Japanese"])
            link_ref = st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link video của đối thủ để AI phân tích...")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="ví dụ: cách làm bánh flan, review iPhone 15")
            link_chan = st.text_input("Link kênh YouTube của bạn (Tùy chọn)", placeholder="ví dụ: https://www.youtube.com/channel/...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Tạo Nội Dung Tối Ưu", key="main_btn"):
            if kw and api_key:
                st.session_state.data['kw'] = kw
                st.session_state.step = 2
                st.rerun()
            else: st.warning("Vui lòng nhập đầy đủ Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 2: TREND PREDICTOR & CÔNG CỤ (Logic mới + Ảnh 844)
# ---------------------------------------------------------
if st.session_state.step >= 2:
    st.markdown(f"### 📈 KẾT QUẢ TỐI ƯU CHO TỪ KHÓA: <span style='color:#f1c40f'>{st.session_state.data['kw'].upper()}</span>", unsafe_allow_html=True)
    
    # Trend Predictor Section
    st.markdown('<p style="font-weight:bold; color:#f1c40f;">🔥 DỰ ĐOÁN XU HƯỚNG (TREND PREDICTOR)</p>', unsafe_allow_html=True)
    tm1, tm2, tm3 = st.columns(3)
    with tm1: st.markdown('<div class="metric-card">Lưu lượng<br><b>Cao (9.2k)</b></div>', unsafe_allow_html=True)
    with tm2: st.markdown('<div class="metric-card">Cạnh tranh<br><b style="color:#e67e22">Trung bình</b></div>', unsafe_allow_html=True)
    with tm3: st.markdown('<div class="metric-card">Xu hướng<br><b style="color:#2ecc71">🚀 ĐANG LÊN</b></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;">🚀 CÔNG CỤ PHÂN TÍCH ĐỐI THỦ:</p>', unsafe_allow_html=True)
    col_btn = st.columns(3)
    col_btn[0].button("Kiểm tra danh mục video", type="secondary")
    col_btn[1].button("Kiểm tra thẻ tag video", type="secondary")
    col_btn[2].button("Thông tin video", type="secondary")

    # 10 Tiêu đề (Ảnh 844/845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    titles = [f"Tiêu đề {i}: {st.session_state.data['kw']} - Bí mật {i} bước để thành công" for i in range(1, 11)]
    for t in titles:
        st.markdown(f'<p style="background:#222533; padding:10px; border-radius:8px; margin-bottom:8px; border-left:3px solid #3498db;">{t}</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Bạn muốn viết mô tả YouTube chuẩn SEO cho tiêu đề nào?")
    sel_t = st.selectbox("Chọn tiêu đề:", titles, label_visibility="collapsed")
    if st.button("Tạo Mô Tả", key="gen_desc"):
        st.session_state.data['selected_title'] = sel_t
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 3: MÔ TẢ & TAGS (Ảnh 846)
# ---------------------------------------------------------
if st.session_state.step >= 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"📝 **MÔ TẢ VIDEO CHUẨN SEO**")
    st.text_area("Nội dung mô tả (Copy):", f"Video này hướng dẫn chi tiết về {st.session_state.data['kw']}...\n\nHãy nhấn Đăng ký kênh để không bỏ lỡ!", height=150)
    
    st.markdown("📊 **25 TỪ KHÓA TỈ LỆ TÌM KIẾM CAO**")
    tags = ["YouTube SEO", "Trending", "Marketing AI", "Content Creator", "Video Viral"] + [f"Tag {i}" for i in range(20)]
    tag_html = "".join([f'<span class="tag-chip">{t}</span>' for t in tags])
    st.markdown(tag_html, unsafe_allow_html=True)
    st.button("Sao chép danh sách Tag", key="copy_tag")
    
    st.markdown("💬 **BÌNH LUẬN GIM BỞI CHỦ KÊNH**")
    st.info("Chào cả nhà! Video này mình dành rất nhiều tâm huyết về chủ đề này. Các bạn thấy sao? Hãy comment bên dưới nhé!")
    
    if st.button("Tiếp theo: Thiết kế Thumbnail"):
        st.session_state.step = 4
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 4: THUMBNAIL PROMPT (Ảnh 847)
# ---------------------------------------------------------
if st.session_state.step >= 4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🎨 **CÔNG CỤ TẠO ẢNH MINH HỌA**")
    txt_thumb = st.text_input("Văn bản trên Thumbnail (Tùy chọn)", placeholder="ví dụ: BÍ MẬT ĐƯỢC TIẾT LỘ")
    
    st.write("Chọn phong cách Thumbnail:")
    st.radio("Style:", ["Ảnh Thật", "3D Render", "Điện Ảnh", "Hoạt Hình", "Tối Giản"], horizontal=True, label_visibility="collapsed")
    
    if st.button("Tạo Prompt Ảnh"):
        st.code(f"/imagine prompt: A high contrast YouTube thumbnail for '{st.session_state.data['kw']}', text '{txt_thumb}', 8k resolution, cinematic lighting --ar 16:9")
    
    st.divider()
    c_dl, c_new = st.columns(2)
    with c_dl: st.button("📥 Tải về báo cáo", type="primary")
    with c_new: 
        if st.button("🔄 Tạo nội dung mới"):
            st.session_state.step = 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Chân trang (Footer)
st.markdown('<p style="text-align:center; color:#555; font-size:12px;">© 2026 Developed by Van Quyet - Giải pháp AI Marketing toàn diện</p>', unsafe_allow_html=True)
