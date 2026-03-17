def seo_score(title, desc):

    score = 0

    if len(title) > 40:
        score += 30
    if "?" in title or "!" in title:
        score += 20
    if len(desc) > 100:
        score += 30
    if "#" in desc:
        score += 20

    return f"SEO Score: {score}/100"
