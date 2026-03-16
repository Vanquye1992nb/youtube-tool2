import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN (SÁNG HƠN, GIỐNG MẪU 100%) ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Thế", layout="centered")

st.markdown("""
    <style>
    /* Nền Slate nhạt giúp các ô nhập liệu nổi bật */
    .stApp { background-color: #f1f5f9; color: #1e293b; }
    
    /* Card chứa nội dung trắng chuẩn mẫu */
    .card { 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    /* Tiêu đề Chuyên Gia SEO Video (Ảnh 843) */
    .title-gold { 
        color: #d97706; 
        font-size: 28px; 
        font-weight: bold; 
        text-align: center; 
        margin-bottom: 5px;
    }
    .subtitle { color: #64748b; text-align: center; margin-bottom: 25px; font-size: 14px; }

    /* Fix lỗi mất tiêu đề ô nhập liệu */
    label { color: #334155 !important; font-weight: 600 !important; margin-bottom: 8px !important; display: block !important; }

    /* Button xanh chuẩn mẫu 843 */
    .stButton>button { 
        border-radius: 8px; 
        height: 3em; 
        font-weight: bold; 
        width: 100%; 
        background-color: #2563eb !important;
        color: white !important;
    }

    /* Thẻ tag bong bóng (Ảnh 846) */
    .tag-chip { 
        background-color: #e2e8f0; 
        color: #1e40af; 
        padding: 5px 12px; 
        border-radius: 15px; 
        display: inline-block; 
        margin: 4px; 
        font-size: 13px;
        border: 1px solid #cbd5e1;
    }
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
    if st.button("🔄 Reset Tool"):
        st.session_state.clear()
        st.rerun()

def safe_generate(prompt):
    try:
        # Cách gọi model an toàn nhất để tránh lỗi 404
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi API: {str(e)}")
        return None

# --- BƯỚC 1: FORM NHẬP LIỆU (Ảnh 1000000843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Đưa video của bạn lên top tìm kiếm YouTube!</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            link_ref = st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link tại đây...", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: cách làm SEO", key="kw_input")
            link_chan = st.text_input("Link kênh YouTube của bạn (Tùy chọn)", key="chan")
        
        if st.button("🚀 Tạo Nội Dung Tối Ưu"):
            if kw and api_key:
                with st.spinner("Đang phân tích..."):
                    prompt = f"Phân tích SEO cho từ khóa '{kw}'. Trả về JSON: 'titles' (list 10), 'tags' (list 25), 'desc', 'comment'."
                    res = safe_generate(prompt)
                    if res:
                        # Bóc tách JSON an toàn
                        match = re.search(r'\{.*\}', res, re.DOTALL)
                        if match:
                            st.session_state.seo_data = json.loads(match.group())
                            st.session_state.current_kw = kw
                            st.session_state.step = 2
                            st.rerun()
            else: st.warning("Vui lòng điền đủ Từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ & CÔNG CỤ (Ảnh 1000000844/846) ---
if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ CHO: {st.session_state.current_kw.upper()}")
    
    # Nút công cụ (Ảnh 844)
    st.write("🛠️ CÔNG CỤ PHÂN TÍCH:")
    bc1, bc2, bc3 = st.columns(3)
    if bc1.button("🔵 Danh mục"): st.info("Danh mục đề xuất: Giáo dục / Công nghệ")
    if bc2.button("🟢 Thẻ Tag"): st.success(", ".join(st.session_state.seo_data.get('tags', [])))
    if bc3.button("🟣 Thông tin"): st.write("Đang quét dữ liệu metadata...")

    # Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for t in st.session_state.seo_data.get('titles', []):
        st.markdown(f"- {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Thẻ Tag (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 TỪ KHÓA TÌM KIẾM CAO**")
    tags_html = "".join([f'<span class="tag-chip">{tag}</span>' for tag in st.session_state.seo_data.get('tags', [])])
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.divider()
    st.text_area("Mô tả SEO:", st.session_state.seo_data.get('desc'), height=150)
    st.info(f"💬 Bình luận ghim: {st.session_state.seo_data.get('comment')}")
    
    if st.button("🎨 Tiếp theo: Tạo Thumbnail"):
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 3: THUMBNAIL (Ảnh 1000000847) ---
if st.session_state.step >= 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🎨 **CÔNG CỤ TẠO ẢNH MINH HỌA**")
    txt_thumb = st.text_input("Văn bản trên Thumbnail", value="SEO TOP 1")
    if st.button("Tạo Prompt"):
        st.code(f"A high-quality YouTube thumbnail for '{st.session_state.current_kw}', bold text '{txt_thumb}', 8k resolution.")
    st.markdown('</div>', unsafe_allow_html=True)
