import google.generativeai as genai
import time
from cachetools import TTLCache

# ===== CONFIG =====
API_KEY = "AIzaSyAoCyxGW6zpwEmQHj4yAHn_6tLzqLbfsqE"

genai.configure(api_key=API_KEY)

# cache 100 request / 10 phút
cache = TTLCache(maxsize=100, ttl=600)

# danh sách model fallback
MODELS = [
    "gemini-1.5-flash",
    "gemini-1.0-pro"
]

# ===== OFFLINE FALLBACK =====
def offline_response(prompt):
    return f"""
⚠️ AI đang lỗi → dùng fallback

👉 Gợi ý nội dung cho:
{prompt}

- Tiêu đề: {prompt} cực hay
- Mô tả: Video chia sẻ về {prompt}
- Hashtag: #youtube #ai #viral
"""

# ===== MAIN FUNCTION =====
def ask_ai(prompt, retries=3):

    # cache check
    if prompt in cache:
        return cache[prompt]

    for attempt in range(retries):

        for model_name in MODELS:

            try:
                model = genai.GenerativeModel(model_name)

                res = model.generate_content(prompt)

                if res and hasattr(res, "text") and res.text:
                    cache[prompt] = res.text
                    return res.text

            except Exception as e:
                print(f"Model {model_name} lỗi: {e}")
                time.sleep(1)

    # fallback cuối cùng
    return offline_response(prompt)
