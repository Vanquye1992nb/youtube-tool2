from ai_engine import ask_ai

def generate_story_script(topic):
    prompt = f"""
    Viết storytelling video giữ chân người xem:
    {topic}
    có hook mạnh và cao trào
    """
    return ask_ai(prompt)
