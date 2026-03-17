from ai_engine import ask_ai

def generate_script(topic):

    prompt=f"""
    viết script video youtube 10 phút
    chủ đề {topic}

    gồm
    hook
    main content
    outro
    """

    return ask_ai(prompt)
