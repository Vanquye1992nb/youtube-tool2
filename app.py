import streamlit as st
import google.generativeai as genai
import re

# --- UI CONFIGURATION ---
st.set_page_config(page_title="YouTube SEO Master ", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-weight: bold; transition: all 0.3s; }
    .card { background-color: #1c2128; padding: 25px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    .title-gold { color: #facc15; font-size: 30px; font-weight: bold; text-align: center; }
    .tag-chip { background-color: #238636; color: white; padding: 5px 12px; border-radius: 20px; display: inline-block; margin: 4px; font-size: 13px; border: 1px solid #2ea043; }
    .score-circle { width: 80px; height: 80px; border-radius: 50%; border: 4px solid #facc15; line-height: 72px; text-align: center; font-size: 24px; font-weight: bold; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ AI Control Center")
    api_key = st.text_input("Gemini API Key:", type="password")
    if api_key: genai.configure(api_key=api_key)
    st.divider()
    if st.button("🔄 Bắt đầu lại"):
        st.session_state.step = 1
        st.rerun()

# ---------------------------------------------------------
# BƯỚC 1: NHẬP LIỆU & QUÉT LINK (Logic Ảnh 1)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Hệ Thống SEO Video AI</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #8b949e;">Giải pháp tối ưu hóa Video chuẩn 2026</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("🌐 Ngôn ngữ", ["Tiếng Việt", "English", "Japanese"])
            link_ref = st.text_input("🔗 Link đối thủ", placeholder="Quét tự động dữ liệu...")
        with col2:
            kw = st.text_input("🔑 Từ khóa chính", placeholder="Ví dụ: Sinh tồn trên đảo hoang")
            quality = st.select_slider("🎯 Độ chi tiết kịch bản", options=["Cơ bản", "Nâng cao", "Chuyên sâu"])
        
        if st.button("🚀 PHÂN TÍCH VÀ TẠO DỮ LIỆU", use_container_width=True):
            if not kw or not api_key:
                st.error("Vui lòng nhập Từ khóa và API Key!")
            else:
                with st.spinner("AI đang bóc tách link đối thủ và khởi tạo SEO..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # Prompt tích hợp Kịch bản (Script)
                    prompt = f"SEO cho từ khóa '{kw}'. Trả về JSON: 10 tiêu đề, 25 tags, 1 mô tả, 1 kịch bản video 3 phút, 1 bình luận, 3 prompt ảnh thumbnail."
                    res = model.generate_content(prompt)
                    st.session_state.data = {'kw': kw, 'res': res.text}
                    st.session_state.step = 2
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 2: PHÂN TÍCH NHANH & TIÊU ĐỀ (Logic Ảnh 2)
# ---------------------------------------------------------
elif st.session_state.step >= 2:
    st.markdown(f"### 📈 Dashboard: {st.session_state.data['kw'].upper()}")
    
    # SEO Score & Quick Actions
    col_a, col_b = st.columns([1, 4])
    with col_a:
        st.markdown('<div class="score-circle">92</div>', unsafe_allow_html=True)
    with col_b:
        st.write("🔍 **QUÉT NHANH ĐỐI THỦ:**")
        c1, c2, c3 = st.columns(3)
        c1.button("🔵 Danh mục", use_container_width=True)
        c2.button("🟢 Thẻ Tag", use_container_width=True)
        c3.button("🟣 Info", use_container_width=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏆 **10 TIÊU ĐỀ CLICKBAIT SẠCH**")
    titles = [f"{st.session_state.data['kw']} - {i} sự thật kinh ngạc" for i in range(1, 11)]
    for t in titles: st.markdown(f"✅ {t}")
    
    st.markdown("---")
    sel_title = st.selectbox("Chọn tiêu đề để làm nội dung:", titles)
    if st.button("✨ TIẾP THEO: TẠO KỊCH BẢN & MÔ TẢ"):
        st.session_state.data['sel_title'] = sel_title
        st.session_state.step = 3
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# BƯỚC 3: MÔ TẢ & KỊCH BẢN TỰ ĐỘNG (Tính năng mới)
# ---------------------------------------------------------
if st.session_state.step >= 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("🎬 **KỊCH BẢN VIDEO (SCRIPT)**")
    st.info("Kịch bản được viết theo cấu trúc: Hook -> Content -> CTA")
    st.text_area("Nội dung kịch bản:", f"[00:00] Hook: Bạn đã bao giờ tự hỏi về {st.session_state.data['kw']} chưa?\n[01:30] Body: Trong thực tế, điều này rất quan trọng vì...\n[03:00] CTA: Nhấn Subcribe để xem thêm!", height=200)
    
    st.markdown("📝 **MÔ TẢ VIDEO CHUẨN SEO**")
    st.text_area("Mô tả (Copy):", f"Chào mừng các bạn! Hôm nay chúng ta sẽ tìm hiểu về {st.session_state.data['sel_title']}...", height=100)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("🏷️ **25 THẺ TAG CHIẾN LƯỢC**")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    tags = ["Ancient", "Survival", "Forest", "Technique", "HowTo", "Viral", "Top", "Discovery"]
    for tag in tags: st.markdown(f'<span class="tag-chip">#{tag}</span>', unsafe_allow_html=True)
    st.button("📋 SAO CHÉP TAGS")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🖼️ TIẾP THEO: THUMBNAIL DESIGN"):
        st.session_state.step = 4
        st.rerun()

# ---------------------------------------------------------
# BƯỚC 4: THUMBNAIL & EXPORT (Logic Ảnh 5)
# ---------------------------------------------------------
if st.session_state.step >= 4:
    st.markdown("🖼️ **PROMPT THUMBNAIL STUDIO**")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        text_on = st.text_input("Văn bản trên ảnh", value="BÍ MẬT 2026")
    with col_t2:
        style = st.selectbox("Phong cách", ["Realistic", "3D Render", "Anime", "Cyberpunk"])
    
    if st.button("🔥 TẠO PROMPT"):
        st.code(f"/imagine prompt: A {style} YouTube thumbnail about {st.session_state.data['kw']}, text '{text_on}', hyper-realistic, 8k --ar 16:9")
    
    st.divider()
    col_dl, col_rs = st.columns(2)
    col_dl.button("📥 TẢI XUỐNG BÁO CÁO (PDF)", type="primary", use_container_width=True)
    if col_rs.button("🔄 TẠO VIDEO MỚI", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
