import streamlit as st

from modules.seo_generator import generate_full_seo
from modules.title_generator import generate_titles
from modules.script_generator import generate_script
from modules.thumbnail_generator import generate_thumbnail_prompt
from modules.keyword_research import keyword_research
from modules.content_planner import create_plan

st.set_page_config(layout="wide")

st.title("YouTube Automation SaaS PRO")

menu = st.sidebar.selectbox(
    "Tools",
    [
        "SEO Generator",
        "Title Generator",
        "Script Generator",
        "Thumbnail Generator",
        "Keyword Research",
        "Content Planner"
    ]
)

if menu == "SEO Generator":

    keyword = st.text_input("Keyword")

    if st.button("Generate"):

        result = generate_full_seo(keyword)

        st.write(result)

if menu == "Title Generator":

    keyword = st.text_input("Keyword")

    if st.button("Generate"):

        result = generate_titles(keyword)

        st.write(result)

if menu == "Script Generator":

    topic = st.text_input("Topic")

    if st.button("Generate"):

        result = generate_script(topic)

        st.write(result)

if menu == "Thumbnail Generator":

    topic = st.text_input("Topic")

    if st.button("Generate"):

        result = generate_thumbnail_prompt(topic)

        st.write(result)

if menu == "Keyword Research":

    topic = st.text_input("Topic")

    if st.button("Research"):

        result = keyword_research(topic)

        st.write(result)

if menu == "Content Planner":

    niche = st.text_input("Channel Topic")

    if st.button("Create Plan"):

        result = create_plan(niche)

        st.write(result)
