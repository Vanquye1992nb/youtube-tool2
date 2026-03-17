from ai_engine import ask_ai

def generate_full_seo(keyword):

    prompt=f"""
    tối ưu SEO youtube cho keyword {keyword}

    tạo
    - 10 title
    - description
    - 20 hashtag
    - 20 keywords
    """

    return ask_ai(prompt)
