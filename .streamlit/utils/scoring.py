def score_christmas_vibes(text):
    nz_keywords = ["pōhutukawa", "BBQ", "beach", "whānau", "gift", "sale", "Santa", "NZ Post", "Kiwi Christmas"]
    return sum(word.lower() in text.lower() for word in nz_keywords)
