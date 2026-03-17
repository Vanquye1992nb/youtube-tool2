import google.generativeai as genai
import time

# API KEY GOOGLE (bạn đang dùng)
API_KEY = "AIzaSyAoCyxGW6zpwEmQHj4yAHn_6tLzqLbfsqE"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(prompt):

    try:
        time.sleep(1)  # chống spam

        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "⚠️ Không có phản hồi từ AI"

    except Exception as e:
        return f"❌ AI Error: {e}"
