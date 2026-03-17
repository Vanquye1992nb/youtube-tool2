from ai_engine_pro import ask_ai

def generate_script(topic):
    prompt = f"Viết script video YouTube 10 phút về: {topic}"
    return ask_ai(prompt)
