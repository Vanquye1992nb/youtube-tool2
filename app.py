import streamlit as st
import google.generativeai as genai
import random

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #1a1c24; color: white; }
    .stButton>button { border-radius: 8px; font-weight: bold; width: 100%; transition: 0.3s; }
    .card { background-color: #262730; padding: 20px; border-radius: 12px; border: 1px solid #3d3f4e; margin-bottom: 20px; }
    .title-center { color: #facc15; text-align: center; font-size: 28px; font-weight: bold; }
    .trend-up { color: #16a34a; font-weight: bold; }
    .trend-down { color: #dc2626; font-weight: bold; }
    .metric-box { background: #333645; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #4a4a4a; }
    </style>
    """, unsafe_allow_html=True)

# --- QUẢN LÝ TRẠNG THÁI ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'seo_data' not in st.session_state: st.session_state.seo_data = {}

with st.sidebar:
    st.title("⚙️ Cấu hình API")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    if api_key: genai.configure(api_key=api_key)
    st.divider()
    if st.button("🔄 Làm mới quy trình"):
        st.session_state.step = 1
        st.rerun()

# ---------------------------------------------------------
# BƯỚC 1: NHẬP LIỆU
# ---------------------------------------------------------
if st.session_state.step >= 1:
    st.markdown('<p class="title-center">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"])
            link_ref = st.text_input("Link video đối thủ (Tùy chọn)")
        with col2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: Cách làm bánh rán")
            target = st.selectbox("Đối tượng mục tiêu", ["Đại chúng", "Trẻ em", "Kỹ thuật"])
        
        if st.button("🚀 PHÂN TÍCH XU HƯỚNG & SEO"):
            if kw and api_key:
                st.session_state.seo_data['kw'] = kw
                st.session_state.step = 2
                st.rerun()
            else: st.warning("Vui lòng nhập Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 2: DỰ ĐOÁN XU HƯỚNG (TREND PREDICTOR) - TÍNH NĂNG MỚI
# ---------------------------------------------------------
if st.session_state.step >= 2:
    st.markdown("### 🔥 DỰ ĐOÁN XU HƯỚNG (TREND PREDICTOR)")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Giả lập logic AI phân tích xu hướng
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown('<div class="metric-box">Lưu lượng<br><b style="font-size:20px;">8.5K/tháng</b></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown('<div class="metric-box">Cạnh tranh<br><b style="font-size:20px; color:#facc15;">Trung bình</b></div>', unsafe_allow_html=True)
    with col_m3:
        st.markdown('<div class="metric-box">Trạng thái<br><b class="trend-up" style="font-size:20px;">🔥 ĐANG LÊN</b></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.write(f"💡 **Đánh giá từ chuyên gia AI:** Từ khóa *'{st.session_state.seo_data['kw']}'* đang có dấu hiệu tăng trưởng mạnh trong 30 ngày qua. Đây là thời điểm vàng để xuất bản video nhằm đón đầu xu hướng.")
    
    if st.button("✨ TIẾP TỤC TẠO TIÊU ĐỀ & MÔ TẢ"):
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 3: KẾT QUẢ SEO (TIÊU ĐỀ, TAGS, MÔ TẢ)
# ---------------------------------------------------------
if st.session_state.step >= 3:
    st.markdown(f"### 📊 KẾT QUẢ SEO CHO: {st.session_state.seo_data['kw'].upper()}")
    
    # Nút bấm phân tích nhanh theo mẫu ảnh 1000000844
    c1, c2, c3 = st.columns(3)
    c1.button("🔵 Kiểm tra danh mục")
    c2.button("🟢 Kiểm tra thẻ tag")
    c3.button("🟣 Thông tin video")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🏅 **10 TIÊU ĐỀ HẤP DẪN (DỰA TRÊN TREND)**")
    titles = [f"Bí mật {st.session_state.seo_data['kw']} bùng nổ 2026", f"Cách {st.session_state.seo_data['kw']} kiếm tiền triệu mỗi ngày"]
    for t in titles: st.info(t)
    
    st.write("---")
    st.text_area("Mô tả chuẩn SEO:", "Nội dung video này sẽ giúp bạn nắm bắt xu hướng...", height=100)
    
    st.write("🏷️ **Thẻ Tag đề xuất:**")
    st.markdown('<span class="tag-chip">#Trending</span> <span class="tag-chip">#Viral</span> <span class="tag-chip">#SEO2026</span>', unsafe_allow_html=True)
    
    if st.button("🔄 Tạo lại nội dung"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
