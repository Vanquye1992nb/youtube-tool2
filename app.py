import streamlit as st
import openai

# ===============================
# CONFIG
# ===============================

st.set_page_config(
    page_title="Trợ Lý YouTube Toàn Năng",
    layout="centered"
)

# nhập API key
openai.api_key = st.secrets.get("OPENAI_API_KEY","")

# ===============================
# HEADER
# ===============================

st.markdown("""
# Trợ Lý **YouTube** Toàn Năng

Công cụ AI tự động hóa phát triển kênh YouTube
""")

st.divider()

# ===============================
# HOME MENU
# ===============================

col1,col2 = st.columns(2)
col3,col4 = st.columns(2)

with col1:
    plan_btn = st.button("📋 Kế hoạch không biên giới")

with col2:
    seo_btn = st.button("📈 Chuyên Gia SEO Video")

with col3:
    branding_btn = st.button("🎨 Cấu hình Logo & Banner")

with col4:
    checklist_btn = st.button("✅ Checklist Xây Dựng Kênh")

st.divider()

# ===============================
# AI FUNCTION
# ===============================

def ask_ai(prompt):

    try:

        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}]
        )

        return response.choices[0].message.content

    except:
        return "AI chưa cấu hình API."

# ===============================
# MODULE 1
# KẾ HOẠCH KÊNH
# ===============================

if plan_btn:

    st.header("📋 Kế hoạch phát triển kênh")

    niche = st.text_input("Chủ đề kênh")

    if st.button("Tạo kế hoạch nội dung"):

        prompt=f"""
        Lập kế hoạch phát triển kênh YouTube
        chủ đề {niche}

        gồm:
        - kế hoạch 30 ngày
        - ý tưởng video
        - chiến lược tăng view
        """

        result=ask_ai(prompt)

        st.write(result)

# ===============================
# MODULE 2
# SEO VIDEO
# ===============================

if seo_btn:

    st.header("📈 Chuyên gia SEO Video")

    keyword = st.text_input("Từ khóa video")

    if st.button("Tạo SEO Video"):

        prompt=f"""
        Tối ưu SEO video youtube với từ khóa {keyword}

        tạo:
        - 10 tiêu đề
        - mô tả SEO
        - 20 hashtag
        - 20 keywords
        """

        result=ask_ai(prompt)

        st.write(result)

# ===============================
# MODULE 3
# BRANDING
# ===============================

if branding_btn:

    st.header("🎨 Tạo Logo & Banner")

    channel_name=st.text_input("Tên kênh")

    niche=st.text_input("Chủ đề kênh")

    if st.button("Tạo ý tưởng branding"):

        prompt=f"""
        Gợi ý logo và banner cho kênh youtube

        tên kênh {channel_name}
        chủ đề {niche}

        gồm:
        - phong cách logo
        - màu sắc
        - banner concept
        """

        result=ask_ai(prompt)

        st.write(result)

# ===============================
# MODULE 4
# CHECKLIST
# ===============================

if checklist_btn:

    st.header("✅ Checklist xây dựng kênh")

    if st.button("Tạo checklist"):

        prompt="""
        tạo checklist xây dựng kênh youtube từ 0 đến 100k subs
        """

        result=ask_ai(prompt)

        st.write(result)
