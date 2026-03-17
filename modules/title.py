from ai_engine import ask_ai

def generate_titles(keyword):
    prompt = f"Tạo 30 tiêu đề YouTube viral cho: {keyword}"
    return ask_ai(prompt)
