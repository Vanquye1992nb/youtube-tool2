import streamlit as st
import google.generativeai as genai
import json
import re

# --- CẤU HÌNH GIAO DIỆN CHUẨN 5 ẢNH ---
st.set_page_config(page_title="Trợ Lý SEO Youtube Văn Quyết", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b313e; color: #ffffff; }
    
    /* Hiện rõ tiêu đề các ô nhập liệu (Fix lỗi ảnh 860) */
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

    /* Nút Tạo nội dung (Ảnh 843) */
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

# --- HÀM AI FIX LỖI 404 TRIỆT ĐỂ ---
def call_ai_final(api_key, keyword):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng model_name đầy đủ và phiên bản ổn định
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Bạn là chuyên gia SEO Youtube. Hãy phân tích từ khóa '{keyword}'.
        Trả về DUY NHẤT 1 chuỗi mã JSON sau:
        {{
            "titles": ["10 tiêu đề hay"],
            "tags": ["25 thẻ tag"],
            "desc": "Mô tả chuẩn SEO",
            "thumb": "Mô tả hình ảnh thumbnail"
        }}
        """
        # Thử gọi bằng phương thức trực tiếp nhất
        response = model.generate_content(prompt)
        
        # Bóc tách JSON an toàn (Sửa lỗi không ra thông tin)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")
        if "404" in str(e):
            st.info("Mẹo: Hãy thử đổi API Key mới hoặc kiểm tra lại quyền truy cập Model Flash trong Google AI Studio.")
        return None

if 'step' not in st.session_state: st.session_state.step = 1

with st.sidebar:
    st.header("🔑 Cài đặt")
    api_key = st.text_input("Gemini API Key:", type="password")

# --- BƯỚC 1: NHẬP LIỆU (Ảnh 843) ---
if st.session_state.step == 1:
    st.markdown('<p class="title-gold">Chuyên Gia SEO Video</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"], key="lang")
            st.text_input("Link video đối thủ", placeholder="Dán link...", key="ref")
        with c2:
            kw = st.text_input("Từ khóa chính", placeholder="Ví dụ: Cách làm giàu", key="kw")
            st.text_input("Link kênh của bạn", key="chan")
        
        if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
            if kw and api_key:
                with st.spinner("Đang phân tích..."):
                    res = call_ai_final(api_key, kw)
                    if res:
                        st.session_state.data = res
                        st.session_state.current_kw = kw
                        st.session_state.step = 2
                        st.rerun()
            else: st.warning("Hãy nhập Từ khóa và Key!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- BƯỚC 2: KẾT QUẢ (Ảnh 844, 845, 846) ---
if st.session_state.step >= 2:
    st.markdown(f"### SEO: {st.session_state.current_kw.upper()}")
    
    # 3 Nút chức năng (Ảnh 844)
    col1, col2, col3 = st.columns(3)
    col1.button("🔵 Danh mục", use_container_width=True)
    col2.button("🟢 Thẻ Tag", use_container_width=True)
    col3.button("🟣 Thông tin", use_container_width=True)

    # 10 Tiêu đề (Ảnh 845)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🏅 **10 TIÊU ĐỀ HẤP DẪN**")
    for t in st.session_state.data.get('titles', []):
        st.write(f"✅ {t}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 25 Tags (Ảnh 846)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("📊 **25 TỪ KHÓA TÌM KIẾM CAO**")
    tags = "".join([f'<span class="tag-chip">{t}</span>' for t in st.session_state.data.get('tags', [])])
    st.markdown(tags, unsafe_allow_html=True)
    
    if st.button("🔄 Quay lại"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
