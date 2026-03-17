import streamlit as st

# import module
from modules.seo import generate_seo
from modules.title import generate_titles
from modules.script import generate_script
from modules.story_script import generate_story_script
from modules.keyword import keyword_research
from modules.plan import content_plan
from modules.thumbnail import thumbnail_prompt
from modules.competitor import analyze_competitor
from modules.seo_score import seo_score

from ai_engine_pro import ask_ai

# ================= CONFIG =================
st.set_page_config(page_title="YouTube PRO Tool", layout="wide")

st.title("🔥 YouTube Automation PRO (Anti Crash)")

# ================= CACHE =================
@st.cache_data(ttl=600)
def cached_ai(prompt):
    return ask_ai(prompt)

# ================= SIDEBAR =================
menu = st.sidebar.selectbox(
    "Chọn chức năng",
    [
        "SEO Video",
        "Title Generator",
        "Script Video",
        "Story Script PRO",
        "Keyword Research",
        "Content Plan",
        "Thumbnail Prompt",
        "Competitor Analysis",
        "SEO Score",
        "Test AI"
    ]
)

# ================= UI FUNCTION =================
def run_with_cache(prompt):
    with st.spinner("⏳ Đang xử lý..."):
        result = cached_ai(prompt)

    if "⚠️" in result:
        st.warning("AI đang fallback")
        st.text(result)
    elif "❌" in result:
        st.error(result)
    else:
        st.success("AI OK")
        st.write(result)

# ================= FEATURES =================

# SEO
if menu == "SEO Video":
    keyword = st.text_input("Nhập keyword")
    if st.button("Generate SEO"):
        run_with_cache(f"SEO YouTube cho: {keyword}")

# TITLE
elif menu == "Title Generator":
    keyword = st.text_input("Nhập chủ đề")
    if st.button("Generate Title"):
        run_with_cache(f"Tạo 30 tiêu đề viral: {keyword}")

# SCRIPT
elif menu == "Script Video":
    topic = st.text_input("Nhập topic")
    if st.button("Generate Script"):
        run_with_cache(f"Viết script video 5-10 phút: {topic}")

# STORY
elif menu == "Story Script PRO":
    topic = st.text_input("Nhập topic")
    if st.button("Generate Story"):
        run_with_cache(f"Viết storytelling giữ chân người xem: {topic}")

# KEYWORD
elif menu == "Keyword Research":
    topic = st.text_input("Nhập topic")
    if st.button("Research"):
        run_with_cache(f"Tìm 30 keyword YouTube: {topic}")

# PLAN
elif menu == "Content Plan":
    niche = st.text_input("Nhập niche")
    if st.button("Create Plan"):
        run_with_cache(f"Lập kế hoạch 30 ngày: {niche}")

# THUMBNAIL
elif menu == "Thumbnail Prompt":
    topic = st.text_input("Nhập topic")
    if st.button("Generate Thumbnail"):
        run_with_cache(f"Prompt thumbnail viral: {topic}")

# COMPETITOR
elif menu == "Competitor Analysis":
    topic = st.text_input("Nhập topic")
    if st.button("Analyze"):
        run_with_cache(f"Phân tích đối thủ YouTube: {topic}")

# SEO SCORE
elif menu == "SEO Score":
    title = st.text_input("Title")
    desc = st.text_area("Description")
    if st.button("Check SEO"):
        st.success(seo_score(title, desc))

# TEST AI
elif menu == "Test AI":
    prompt = st.text_input("Test prompt")
    if st.button("Run Test"):
        run_with_cache(prompt)
