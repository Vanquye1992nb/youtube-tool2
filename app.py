import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (CHÍNH XÁC THEO MẪU 5 ẢNH) ---
st.set_page_config(page_title="Trợ Lý Videos SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    /* Nền màu Slate chuẩn ảnh gốc */
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Card nội dung */
    .card { 
        background-color: #363d4a; 
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    /* Tiêu đề Gold (Ảnh 843) */
    .title-gold { color: #f1c40f; font-size: 28px; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #bdc3c7; text-align: center; margin-bottom: 25px; font-size: 14px; }

    /* Fix lỗi mất tiêu đề các ô nhập liệu */
    .stTextInput label, .stSelectbox label { 
        color: #ffffff !important; 
        font-weight: 500 !important; 
        display: block !important; 
        padding-bottom: 5px;
    }

    /* Nút Tạo nội dung (Xanh dương - Ảnh 843) */
    .stButton>button { 
        border-radius: 8px; height: 3.5em; font-weight: bold; width: 100%; 
        background-color: #2563eb !important; color: white !important; border: none;
    }

    /* Nút phân tích (Xanh dương, Xanh lá, Tím - Ảnh 844) */
    .btn-check-blue button { background-color: #3b82f6 !important; color: white !important; }
    .btn-check-green button { background-color: #10b981 !important; color: white !important; }
    .btn-check-purple button { background-color: #a855f7 !important; color: white !important; }

    /* Thẻ Tag (Xám trắng - Ảnh 846) */
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 5px 12px; 
        border-radius: 20px; display: inline-block; margin: 4px; font-size: 12px; border: 1px solid #718096;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO AI ---
def init_ai(api_key):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng phương thức an toàn nhất để tránh 404
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Lỗi khởi tạo AI: {e}")
        return None

# --- QUẢN LÝ SESSION ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'seo_data' not in st.session_state: st.session_state.seo_data = {}

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

# ---------------------------------------------------------
# BƯỚC 1: FORM NHẬP LIỆU (Giống Ảnh 1000000843)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Đưa video của bạn lên top tìm kiếm YouTube!</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            link_ref = st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link tại đây...")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="ví dụ: cách làm giàu")
            link_chan = st.text_input("Link kênh YouTube của bạn (Tùy chọn)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Tạo Nội Dung Tối Ưu"):
            if kw and api_key:
                model = init_ai(api_key)
                if model:
                    with st.spinner("Đang phân tích..."):
                        # Prompt tối ưu để AI trả về JSON sạch
                        prompt = f"Phân tích SEO Youtube '{kw}'. Trả về JSON: 'titles' (10 cái), 'tags' (25 cái), 'desc', 'comment'."
                        try:
                            res = model.generate_content(prompt)
                            match = re.search(r'\{.*\}', res.text, re.DOTALL)
                            if match:
                                st.session_state.seo_data = json.loads(match.group())
                                st.session_state.current_kw = kw
                                st.session_state.step = 2
                                st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi API: {e}. Vui lòng kiểm tra lại Key hoặc Model.")
            else: st.warning("Vui lòng điền đủ Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 2: KẾT QUẢ (Giống Ảnh 1000000844 -> 846)
# ---------------------------------------------------------
if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ TỐI ƯU: <span style='color:#f1c40f'>{st.session_state.current_kw.upper()}</span>", unsafe_allow_html=True)
    
    # Nút công cụ (Ảnh 844)
    st.write("🚀 CÔNG CỤ PHÂN TÍCH ĐỐI THỦ:")
    bc1, bc2, bc3 = st.columns(3)
    with bc1: st.markdown('<div class="btn-check-blue">', unsafe_allow_html=True); st.button("Kiểm tra danh mục video"); st.markdown('</div>', unsafe_allow_html=True)
    with bc2: st.markdown('<div class="btn-check-green">', unsafe_allow_html=True); st.button("Kiểm tra thẻ tag video"); st.markdown('</div>', unsafe_allow_html=True)
    with bc3: st.markdown('<div class="btn-check-purple">', unsafe_allow_html=True); st.button("Thông tin video"); st.markdown('</div>', unsafe_allow_html=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for i, t in enumerate(st.session_state.seo_data.get('titles', [])):
        st.markdown(f"<div style='background:#2d3748; padding:8px; border-radius:5px; margin-bottom:5px; border-left:4px solid #f1c40f;'>{t}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Thẻ Tag (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📈 **25 TỪ KHÓA TÌM KIẾM CAO**")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in st.session_state.seo_data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.divider()
    st.text_area("Mô tả SEO:", st.session_state.seo_data.get('desc'), height=150)
    st.info(f"💬 Bình luận: {st.session_state.seo_data.get('comment')}")
    
    if st.button("🎨 Tiếp theo: Thumbnail"):
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
