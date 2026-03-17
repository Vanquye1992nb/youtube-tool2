from ai_engine import ask_ai

def analyze_competitor(topic):
    prompt = f"""
    Phân tích video top YouTube về: {topic}

    - insight nội dung
    - điểm mạnh
    - điểm yếu
    """
    return ask_ai(prompt)
