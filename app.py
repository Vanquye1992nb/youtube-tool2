import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN MỚI (GIẢM ĐỘ TỐI - SANG TRỌNG) ---
st.set_page_config(page_title="SEO Youtube Pro", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #2b303b; color: #f1f1f1; }
    .stApp { background-color: #2b303b; }
    
    /* Khối Card màu sáng hơn */
    .card { 
        background-color: #363d4a; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #4a5568; 
        margin-bottom: 20px;
    }
    
    /* Tiêu đề Gold Amber */
    .title-gold { 
        color: #fbbf24; 
        font-size: 32px; 
        font-weight: 800; 
        text-align: center; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Thẻ Tag Chips xanh sáng */
    .tag-chip { 
        background-color: #4a5568; 
        color: #63b3ed; 
        padding: 5px 12px; 
        border-radius: 20px; 
        display: inline-block; 
        margin: 4px; 
        border: 1px solid #718096; 
        font-size: 13px;
    }

    /* Button Support ngang chuẩn mẫu */
    .stButton>button { 
        border-radius: 8px; 
        font-weight: bold; 
        transition: 0.3s; 
        border: 1px solid #4a5568;
    }
    .btn-action { background-color: #4a5568 !important; color: #fbbf24 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- QUẢN LÝ DỮ LIỆU ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'seo_results' not in st.session_state: st.session_state.seo_results = {}

with st.sidebar:
    st.header("🔑 Cấu Hình")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    if api_key: genai.configure(api_key=api_key)
    if st.button("🔄 Làm mới"):
        st.session_state.clear()
        st.rerun()

def get_ai_response(prompt):
    if not api_key:
        st.error("Chưa có API Key!")
        return None
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi: {e}")
        return None

# ---------------------------------------------------------
# GIAI ĐOẠN 1: NHẬP LIỆU (Ảnh 1000000843)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">CHUYÊN GIA SEO VIDEO</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
            link_ref = st.text_input("Link đối thủ", placeholder="https://youtube.com/...")
        with col2:
            kw = st.text_input("Từ khóa chính", placeholder="Ví dụ: Cách làm bánh")
            link_chan = st.text_input("Link kênh của bạn")
        
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                with st.spinner("Đang phân tích dữ liệu..."):
                    # Yêu cầu AI trả về cấu trúc JSON để bóc tách chính xác
                    prompt = f"""
                    Phân tích từ khóa '{kw}' và video đối thủ '{link_ref}'. 
                    Trả về kết quả dưới dạng JSON có các key: 
                    'titles' (list 10 cái), 'tags' (list 25 cái), 'desc' (chuỗi), 
                    'category' (chuỗi), 'comment' (chuỗi), 'trend_score' (số 1-100).
                    """
                    raw_res = get_ai_response(prompt)
                    if raw_res:
                        # Clean JSON code block if AI includes it
                        clean_json = re.sub(r'```json|```', '', raw_res).strip()
                        try:
                            st.session_state.seo_results = json.loads(clean_json)
                            st.session_state.kw = kw
                            st.session_state.step = 2
                            st.rerun()
                        except:
                            st.error("AI trả về sai định dạng. Hãy thử nhấn lại!")
            else: st.warning("Hãy nhập từ khóa và API Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# GIAI ĐOẠN 2 & 3: KẾT QUẢ & CÔNG CỤ (Ảnh 1000000844/846)
# ---------------------------------------------------------
if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ CHO: <span style='color:#fbbf24'>{st.session_state.kw.upper()}</span>", unsafe_allow_html=True)
    
    # Trend Predictor Badge
    score = st.session_state.seo_results.get('trend_score', 50)
    st.write(f"🔥 **Chỉ số xu hướng:** {score}/100 - {'Nên làm ngay!' if score > 70 else 'Cần tối ưu thêm'}")

    # CÁC NÚT HỖ TRỢ PHÂN TÍCH (Ảnh 844)
    st.write("🛠️ **CÔNG CỤ HỖ TRỢ:**")
    c1, c2, c3 = st.columns(3)
    if c1.button("🔵 Danh mục video"): 
        st.info(f"Danh mục đề xuất: {st.session_state.seo_results.get('category')}")
    if c2.button("🟢 Thẻ Tag video"): 
        tags = st.session_state.seo_results.get('tags', [])
        st.success(", ".join(tags))
    if c3.button("🟣 Thông tin video"): 
        st.write(f"Link đối thủ: {link_ref if 'link_ref' in locals() else 'N/A'}")

    # 10 TIÊU ĐỀ (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🏅 **10 TIÊU ĐỀ HẤP DẪN**")
    for i, t in enumerate(st.session_state.seo_results.get('titles', [])):
        st.markdown(f"**{i+1}.** {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    # MÔ TẢ & TAGS (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("📝 **MÔ TẢ VIDEO**")
    st.text_area("Copy mô tả:", st.session_state.seo_results.get('desc'), height=150)
    
    st.markdown("🏷️ **25 TỪ KHÓA TÌM KIẾM CAO**")
    all_tags = st.session_state.seo_results.get('tags', [])
    tag_html = "".join([f'<span class="tag-chip">#{t}</span>' for t in all_tags])
    st.markdown(tag_html, unsafe_allow_html=True)
    st.button("📋 Sao chép danh sách Tag")
    
    st.markdown("💬 **BÌNH LUẬN GIM**")
    st.info(st.session_state.seo_results.get('comment'))
    
    if st.button("🎨 Tiếp theo: Tạo Thumbnail"):
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# GIAI ĐOẠN 4: THUMBNAIL PROMPT (Ảnh 1000000847)
# ---------------------------------------------------------
if st.session_state.step >= 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🎨 **TẠO PROMPT ẢNH THUMBNAIL**")
    txt_on = st.text_input("Chữ trên ảnh", value="BÍ MẬT")
    style = st.radio("Phong cách:", ["Realistic", "3D", "Anime"], horizontal=True)
    
    if st.button("🔥 Tạo Prompt AI"):
        prompt_thumb = f"A professional YouTube thumbnail for '{st.session_state.kw}', with bold text '{txt_on}', style {style}, 8k resolution, cinematic lighting --ar 16:9"
        st.code(prompt_thumb)
    
    st.divider()
    if st.button("🔄 Làm Video Mới"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
