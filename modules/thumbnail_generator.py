from ai_engine import ask_ai

def generate_thumbnail_prompt(topic):

    prompt=f"""
    tạo prompt thumbnail youtube
    chủ đề {topic}
    cinematic lighting
    viral style
    """

    return ask_ai(prompt)
