from ai_engine import ask_ai

def keyword_research(topic):

    prompt=f"""
    tìm 30 keyword youtube
    liên quan tới {topic}
    """

    return ask_ai(prompt)
