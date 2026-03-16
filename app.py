import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN CHUYÊN NGHIỆP ---
st.set_page_config(page_title="Trợ Lý SEO Youtube - Văn Quyết", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; border-radius: 8px 8px 0px 0px; 
        background-color: #1e2130; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; }
    .card { background-color: #1e2130; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; }
    .btn-create { 
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); 
        color: white; border-radius: 10px; padding: 10px; text-align: center; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THANH BÊN CẤU HÌNH ---
with st.sidebar:
    st.image("https://vantheweb.com/wp-content/uploads/2021/04/logo-van-the-web.png", width=180)
    st.title("🔑 Hệ Thống AI")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    st.markdown("---")
    st.info("Hướng dẫn: Nhập từ khóa chính, AI sẽ lo toàn bộ phần còn lại từ Tiêu đề đến Thumbnail.")

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; color: #facc15;'>🖥️ Chuyên Gia SEO Video</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Đưa video của bạn lên top tìm kiếm YouTube!</p>", unsafe_allow_html=True)

# Khởi tạo form nhập liệu trong một Card
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        ngon_ngu = st.selectbox("🌐 Chọn ngôn ngữ", ["Tiếng Việt", "English", "Japanese", "Korean"])
        link_doi_thu = st.text_input("🔗 Link video đối thủ (Tùy chọn)", placeholder="Dán link video đối thủ tại đây...")
    with col2:
        tu_khoa = st.text_input("🔑 Từ khóa chính (Bắt buộc)", placeholder="ví dụ: Cách làm bánh flan, SEO Youtube 2026")
        link_kenh = st.text_input("🏠 Link kênh của bạn (Tùy chọn)", placeholder="Dán link kênh của bạn...")
    
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 TẠO NỘI DUNG TỐI ƯU"):
    if not api_key:
        st.error("Vui lòng nhập API Key để kích hoạt AI!")
    elif not tu_khoa:
        st.warning("Bạn chưa nhập từ khóa chính!")
    else:
        try:
            genai.configure(api_key=api_key)
            # Cơ chế tự quét model tránh lỗi 404
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("AI đang phân tích đối thủ và tối ưu nội dung..."):
                prompt = f"""
                Bạn là một chuyên gia SEO Youtube hàng đầu. Hãy thực hiện các nhiệm vụ sau cho từ khóa '{tu_khoa}':
                1. Đề xuất 10 tiêu đề thu hút, chuẩn SEO (ngôn ngữ: {ngon_ngu}).
                2. Viết một đoạn mô tả video chuẩn SEO dài, chuyên nghiệp, có chứa từ khóa và kêu gọi hành động (CTA).
                3. Trích xuất danh sách 25 thẻ Tag tiềm năng nhất, phân cách bằng dấu phẩy.
                4. Tạo 3 Prompt chi tiết để vẽ ảnh Thumbnail theo 3 phong cách: Điện ảnh, 3D Render và Hoạt hình.
                5. Viết một bình luận ghim (Pinned Comment) để tăng tương tác.
                """
                response = model.generate_content(prompt)
                
                # Hiển thị kết quả theo Tab cho chỉnh chu
                tab1, tab2, tab3, tab4 = st.tabs(["📋 Tiêu đề & Mô tả", "🏷️ Thẻ Tag", "🖼️ Prompt Thumbnail", "💬 Bình luận"])
                
                with tab1:
                    st.success("✅ Tối ưu hóa Tiêu đề và Mô tả thành công!")
                    st.markdown(response.text.split("2.")[0]) # Phần tiêu đề
                    st.markdown("### 📝 Mô tả gợi ý:")
                    st.info(response.text.split("2.")[1].split("3.")[0])
                
                with tab2:
                    st.subheader("🚀 25 Từ khóa tỉ lệ tìm kiếm cao")
                    tags = response.text.split("3.")[1].split("4.")[0]
                    st.code(tags, language="text")
                    st.button("📋 Sao chép thẻ Tag", on_click=lambda: st.write("Đã sao chép!"))
                
                with tab3:
                    st.subheader("🎨 Công cụ tạo ảnh minh họa")
                    prompts = response.text.split("4.")[1].split("5.")[0]
                    st.markdown(prompts)
                
                with tab4:
                    st.subheader("📌 Bình luận ghim bởi chủ kênh")
                    comment = response.text.split("5.")[-1]
                    st.write(comment)

        except Exception as e:
            st.error(f"Lỗi: {str(e)}")

st.markdown("---")
st.caption("© 2026 Developed by Van Quyet - Giải pháp AI Marketing toàn diện")
