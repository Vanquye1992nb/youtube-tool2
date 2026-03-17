import google.generativeai as genai
import time

# ⚠️ ĐỔI KEY MỚI nếu cần
API_KEY = "AIzaSyA65zPoRhCDUDblBof1LCejpc-HZbZNcFQ"

genai.configure(api_key=API_KEY)

# MODEL ƯU TIÊN
MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro-latest",
    "gemini-1.0-pro"
]

def ask_ai(prompt, debug=False):

    for model_name in MODELS:
        try:
            model = genai.GenerativeModel(model_name)

            response = model.generate_content(prompt)

            # trả text chắc chắn
            text = getattr(response, "text", None)

            if text and len(text.strip()) > 10:
                return text

        except Exception as e:
            if debug:
                return f"❌ Lỗi model {model_name}: {e}"
            time.sleep(1)

    return "❌ AI ERROR: API key/model không hoạt động"
