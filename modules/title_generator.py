from ai_engine import ask_ai

def generate_titles(keyword):

    prompt=f"""
    tạo 30 tiêu đề youtube viral
    keyword {keyword}
    """

    return ask_ai(prompt)
