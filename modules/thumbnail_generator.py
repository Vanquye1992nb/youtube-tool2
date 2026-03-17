from ai_engine import ask_ai

def thumbnail_prompt(topic):
    prompt = f"""
    Viết prompt tạo thumbnail YouTube cực viral:
    {topic}
    style cinematic, high contrast
    """
    return ask_ai(prompt)
