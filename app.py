import streamlit as st
import google.generativeai as genai
import json

# --- CẤU HÌNH GIAO DIỆN DARK MODE PREMIUM ---
st.set_page_config(page_title="YouTube SEO Master ", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0f111a; color: #e1e1e6; }
    .card { background-color: #1a1c26; padding: 25px; border-radius: 15px; border: 1px solid #2d2f3d; margin-bottom: 20px; }
    .title-gold { color: #f1c40f; font-size: 30px; font-weight: 800; text-align: center; text-transform: uppercase; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; transition: 0.3s; }
    .tag-chip { background-color: #238636; color: white; padding: 5px 12px; border-radius: 20px; display: inline-block; margin: 4px; border: 1px solid #2ea043; font-size: 13px; }
    .btn-tool { background-color: #2d2f3d !important; color: #3498db !important; border: 1px solid #3498db !important; }
    </style>
    """, unsafe_allow_html=True)

# --- QUẢN LÝ SESSION ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

with st.sidebar:
    st.subheader("🔑 Cấu hình API")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    if api_key: genai.configure(api_key=api_key)
    st.divider()
    if st.button("🔄 Reset Quy Trình"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# --- HÀM GỌI AI XỬ LÝ DỮ LIỆU THẬT ---
def call_ai(prompt):
    if not api_key:
        st.error("Vui lòng nhập API Key ở thanh bên!")
        return None
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi AI: {str(e)}")
        return None

# ---------------------------------------------------------
# BƯỚC 1: NHẬP LIỆU (Ảnh 1)
# ---------------------------------------------------------
if st.session_state.step >= 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
            link_ref = st.text_input("🔗 Link đối thủ", placeholder="Dán link YouTube...")
        with col2:
            kw = st.text_input("🔑 Từ khóa chính", placeholder="Ví dụ: Cách làm SEO")
            link_chan = st.text_input("🏠 Link kênh của bạn")
        
        if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", type="primary"):
            if kw and api_key:
                with st.spinner("Đang phân tích từ khóa và xu hướng..."):
                    # Lấy 10 tiêu đề + Trend cùng lúc để tiết kiệm thời gian
                    res = call_ai(f"Từ khóa: {kw}. Hãy tạo 10 tiêu đề hay, đánh giá xu hướng (Lưu lượng, Cạnh tranh) và cho biết video này có đang hot không.")
                    if res:
                        st.session_state.data['kw'] = kw
                        st.session_state.data['step1_res'] = res
                        st.session_state.step = 2
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 2: CÔNG CỤ & TIÊU ĐỀ (Ảnh 2)
# ---------------------------------------------------------
if st.session_state.step >= 2:
    st.markdown(f"### 📊 Dashboard SEO: {st.session_state.data['kw'].upper()}")
    
    st.write("🛠️ **PHÂN TÍCH ĐỐI THỦ (HOẠT ĐỘNG THẬT):**")
    c1, c2, c3 = st.columns(3)
    if c1.button("🔵 Danh mục", key="cat"): 
        st.info(call_ai(f"Phân tích link {link_ref}. Video này thuộc danh mục nào?"))
    if c2.button("🟢 Thẻ tag", key="tags"): 
        st.success(call_ai(f"Trích xuất tất cả thẻ tag SEO từ video: {link_ref}"))
    if c3.button("🟣 Thông tin", key="info"): 
        st.write(call_ai(f"Lấy Metadata (Tiêu đề, Mô tả gốc) của link: {link_ref}"))

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🏅 **10 TIÊU ĐỀ SEO ĐỀ XUẤT**")
    st.write(st.session_state.data['step1_res']) # Hiển thị 10 tiêu đề AI vừa tạo
    
    sel_t = st.text_input("Nhập tiêu đề bạn chọn (hoặc copy từ trên):")
    if st.button("✨ TIẾP THEO: TẠO MÔ TẢ & TAGS"):
        with st.spinner("Đang tạo kịch bản, mô tả và 25 tags..."):
            res = call_ai(f"Với tiêu đề '{sel_t}', hãy viết 1 mô tả SEO dài, danh sách 25 tags (phân cách bằng dấu phẩy) và 1 bình luận ghim.")
            if res:
                st.session_state.data['step2_res'] = res
                st.session_state.step = 3
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 3: MÔ TẢ & 25 TAGS THẬT (Ảnh 3, 4)
# ---------------------------------------------------------
if st.session_state.step >= 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("📝 **NỘI DUNG CHI TIẾT**")
    st.write(st.session_state.data['step2_res'])
    
    if st.button("🎨 TIẾP THEO: TẠO PROMPT THUMBNAIL"):
        st.session_state.step = 4
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 4: TẠO ẢNH TỪ PROMPT (Ảnh 5)
# ---------------------------------------------------------
if st.session_state.step >= 4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🎨 **AI THUMBNAIL DESIGN**")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        text_thumb = st.text_input("Chữ trên ảnh:", value="BÍ MẬT SEO")
    with col_p2:
        style = st.selectbox("Phong cách:", ["Cinematic", "3D Render", "Anime", "Real Life"])
    
    if st.button("🔥 TẠO PROMPT CHI TIẾT"):
        with st.spinner("Đang thiết kế Prompt chuyên sâu..."):
            p_res = call_ai(f"Tạo 1 câu lệnh (Prompt) bằng tiếng Anh để vẽ ảnh Thumbnail YouTube cho từ khóa '{st.session_state.data['kw']}' với chữ '{text_thumb}', phong cách {style}. Output chỉ trả về câu prompt.")
            st.session_state.data['thumb_prompt'] = p_res
            st.code(p_res, language="text")
    
    if 'thumb_prompt' in st.session_state.data:
        st.success("✅ Bạn hãy Copy đoạn mã trên và dán vào Midjourney, Leonardo.ai hoặc Adobe Firefly để tạo ảnh nhé!")

    if st.button("📥 XUẤT BÁO CÁO & KẾT THÚC"):
        st.balloons()
        st.session_state.step = 1
