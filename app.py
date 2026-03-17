import streamlit as st

from seo_tools import generate_seo
from seo_tools import generate_script
from seo_tools import generate_thumbnail_prompt

from content_plan import create_content_plan


st.set_page_config(
    page_title="YouTube Automation Tool",
    layout="wide"
)

st.title("🚀 YouTube Automation Tool")

menu=st.sidebar.selectbox(
    "Chọn chức năng",
    [
        "SEO Video",
        "Video Script",
        "Thumbnail Prompt",
        "Content Plan"
    ]
)

# SEO VIDEO

if menu=="SEO Video":

    st.header("YouTube SEO Generator")

    keyword=st.text_input("Keyword")

    if st.button("Generate SEO"):

        result=generate_seo(keyword)

        st.write(result)

# SCRIPT

if menu=="Video Script":

    st.header("Video Script Generator")

    topic=st.text_input("Video Topic")

    if st.button("Generate Script"):

        result=generate_script(topic)

        st.write(result)

# THUMBNAIL

if menu=="Thumbnail Prompt":

    st.header("Thumbnail Prompt")

    topic=st.text_input("Topic")

    if st.button("Generate Prompt"):

        result=generate_thumbnail_prompt(topic)

        st.write(result)

# CONTENT PLAN

if menu=="Content Plan":

    st.header("30 Day Content Plan")

    niche=st.text_input("Channel Topic")

    if st.button("Create Plan"):

        result=create_content_plan(niche)

        st.write(result)
