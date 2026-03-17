import streamlit as st

from seo_tools import generate_seo
from script_tools import generate_script
from content_plan import generate_plan
from thumbnail_tools import generate_thumbnail

st.set_page_config(
    page_title="YouTube Automation Tool PRO",
    layout="wide"
)

st.title("🚀 YouTube Automation Tool PRO")

menu = st.sidebar.selectbox(
    "Chọn công cụ",
    [
        "SEO Video",
        "Video Script",
        "Thumbnail Prompt",
        "Content Plan 30 Days"
    ]
)

# SEO TOOL

if menu=="SEO Video":

    st.header("SEO Video Generator")

    keyword=st.text_input("Keyword video")

    if st.button("Generate SEO"):

        if keyword:

            with st.spinner("AI đang tạo SEO..."):

                result=generate_seo(keyword)

            st.write(result)

        else:

            st.warning("Nhập keyword")

# SCRIPT

if menu=="Video Script":

    st.header("Video Script Generator")

    topic=st.text_input("Video Topic")

    if st.button("Generate Script"):

        if topic:

            with st.spinner("AI đang viết script..."):

                result=generate_script(topic)

            st.write(result)

        else:

            st.warning("Nhập topic")

# THUMBNAIL

if menu=="Thumbnail Prompt":

    st.header("Thumbnail Prompt")

    topic=st.text_input("Thumbnail topic")

    if st.button("Generate Prompt"):

        result=generate_thumbnail(topic)

        st.write(result)

# CONTENT PLAN

if menu=="Content Plan 30 Days":

    st.header("30 Day YouTube Plan")

    niche=st.text_input("Channel niche")

    if st.button("Generate Plan"):

        result=generate_plan(niche)

        st.write(result)
