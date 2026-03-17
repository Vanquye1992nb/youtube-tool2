from openai import OpenAI
import streamlit as st

def ask_ai(prompt):

    api_key = st.secrets.get("OPENAI_API_KEY","")

    if api_key == "":
        return "API key missing"

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    return response.choices[0].message.content
