from ai_engine_pro import ask_ai

def generate_seo(keyword):
    prompt = f"""
    SEO YouTube cho: {keyword}

    - 10 tiêu đề
    - mô tả chuẩn SEO
    - 20 hashtag
    - 20 keyword
    """
    return ask_ai(prompt)
