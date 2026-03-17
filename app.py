import streamlit as st

from modules.seo import generate_seo
from modules.title import generate_titles
from modules.script import generate_script
from modules.story_script import generate_story_script
from modules.keyword import keyword_research
from modules.plan import content_plan
from modules.thumbnail import thumbnail_prompt
from modules.competitor import analyze_competitor
from modules.seo_score import seo_score

st.set_page_config(layout="wide")

st.title("🚀 YouTube Automation SaaS PRO+")

menu = st.sidebar.selectbox(
    "Chức năng",
    [
        "SEO Video",
        "Title Generator",
        "Script Video",
        "Story Script PRO",
        "Keyword Research",
        "Content Plan",
        "Thumbnail Prompt",
        "Competitor Analysis",
        "SEO Score"
    ]
)

# SEO
if menu == "SEO Video":
    keyword = st.text_input("Keyword")
    if st.button("Generate"):
        st.write(generate_seo(keyword))

# TITLE
elif menu == "Title Generator":
    keyword = st.text_input("Topic")
    if st.button("Generate"):
        st.write(generate_titles(keyword))

# SCRIPT
elif menu == "Script Video":
    topic = st.text_input("Topic")
    if st.button("Generate"):
        st.write(generate_script(topic))

# STORY
elif menu == "Story Script PRO":
    topic = st.text_input("Topic")
    if st.button("Generate"):
        st.write(generate_story_script(topic))

# KEYWORD
elif menu == "Keyword Research":
    topic = st.text_input("Topic")
    if st.button("Research"):
        st.write(keyword_research(topic))

# PLAN
elif menu == "Content Plan":
    niche = st.text_input("Niche")
    if st.button("Create"):
        st.write(content_plan(niche))

# THUMBNAIL
elif menu == "Thumbnail Prompt":
    topic = st.text_input("Topic")
    if st.button("Generate"):
        st.write(thumbnail_prompt(topic))

# COMPETITOR
elif menu == "Competitor Analysis":
    topic = st.text_input("Topic")
    if st.button("Analyze"):
        st.write(analyze_competitor(topic))

# SEO SCORE
elif menu == "SEO Score":
    title = st.text_input("Title")
    desc = st.text_area("Description")
    if st.button("Check"):
        st.success(seo_score(title, desc))
