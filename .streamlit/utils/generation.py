from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

groq_client = Groq(api_key=GROQ_API_KEY)

def generate_creative_lines(topics, sentiment_summary, trending_post):
    prompt = f"""
You are a creative assistant helping New Zealand retailers connect with shoppers during the Christmas season.

Use the following data:
- Trending hashtags: {topics}
- Sentiment summary (1=positive, 0=negative): {sentiment_summary}
- Sample post: "{trending_post}"

Generate 3 short, emotionally resonant, cheeky, and Kiwi-flavoured social lines that reflect current retail vibes.

Tone: festive, dry, relatable, and stress-aware. Avoid clichés. Prioritise emotional truth and campaign utility.
"""
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
