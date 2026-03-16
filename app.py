import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN 5 ẢNH ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Quyết", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Hiện rõ tiêu đề các ô nhập liệu (Sửa lỗi ảnh 860) */
    label, .stMarkdown p { 
        color: #ffffff !important; 
        font-weight: bold !important; 
        display: block !important; 
    }

    .card { 
        background-color: #363d4a; padding: 25px; 
        border-radius: 12px; border: 1px solid #4a5568; margin-bottom: 20px;
    }

    .title-gold { color: #f1c40f; font-size: 28px; font-weight: 800; text-align: center; }

    /* Nút Tạo nội dung Xanh dương (Ảnh 843) */
    .stButton>button { 
        background-color: #2563eb !important; color: white !important; 
        width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; border: none;
    }

    /* Thẻ tag bong bóng (Ảnh 846) */
    .tag-chip { 
        background-color: #4a5568; color: #e2e8f0; padding: 5px 12px; 
        border-radius: 15px; display: inline-block; margin: 4px; border: 1px solid #718096;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM AI FIX LỖI 404 & KHÔNG RA TIN ---
def call_ai_final(api_key, keyword):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng model_name đầy đủ để ép hệ thống nhận diện đúng (Fix 404)
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')
        
        prompt = f"Phân tích SEO Youtube cho từ khóa '{keyword}'. Trả về JSON: 'titles' (list 10), 'tags' (list 25), 'desc', 'thumb_prompt'."
        response = model.generate_content(prompt)
        
        # Bóc tách JSON an toàn (Fix lỗi không ra tin)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        st.error(f"Lỗi API: {str(e)}")
        return None

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("Gemini API Key:", type="password")

# --- BƯỚC 1: FORM NHẬP LIỆU (Ảnh 843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            st.text_input("Link video đối thủ (Tùy chọn)", placeholder="Dán link...", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính (Bắt buộc)", placeholder="Ví dụ: Cách làm giàu", key="kw")
            st.text_input("Link kênh của bạn", key="chan")
        
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                with st.spinner("Đang phân tích dữ liệu SEO..."):
                    res = call_ai_final(api_key, kw)
                    if res:
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
            else: st.warning("Vui lòng nhập Từ khóa và Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ (Ảnh 844, 845, 846, 847) ---
if st.session_state.step >= 2:
    st.markdown(f"### KẾT QUẢ SEO: {st.session_state.current_kw.upper()}")
    
    # 3 Nút chức năng (Ảnh 844)
    col1, col2, col3 = st.columns(3)
    col1.button("🔵 Danh mục", use_container_width=True)
    col2.button("🟢 Thẻ Tag", use_container_width=True)
    col3.button("🟣 Thông tin", use_container_width=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ YOUTUBE HẤP DẪN**")
    for t in st.session_state.data.get('titles', []):
        st.info(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 25 Tags (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 TỪ KHÓA TÌM KIẾM CAO**")
    tags = "".join([f'<span class="tag-chip">{t}</span>' for t in st.session_state.data.get('tags', [])])
    st.markdown(tags, unsafe_allow_html=True)
    
    # Thumbnail (Ảnh 847)
    st.divider()
    st.write("🎨 **PROMPT TẠO THUMBNAIL:**")
    st.success(st.session_state.data.get('thumb_prompt', 'YouTube Thumbnail Design'))
    
    if st.button("🔄 Tạo từ khóa mới"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
