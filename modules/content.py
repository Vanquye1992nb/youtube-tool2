from ai_engine import ask_ai

def create_plan(niche):

    prompt=f"""
    lập kế hoạch youtube 30 ngày
    chủ đề {niche}
    """

    return ask_ai(prompt)
