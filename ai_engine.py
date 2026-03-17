from openai import OpenAI
import streamlit as st

def ask_ai(prompt):

    if "OPENAI_API_KEY" not in st.secrets:
        return "⚠️ OPENAI_API_KEY chưa cấu hình"

    api_key = st.secrets["OPENAI_API_KEY"]

    client = OpenAI(api_key=api_key)

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI Error: {e}"
