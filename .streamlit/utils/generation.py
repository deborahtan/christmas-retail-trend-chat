from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

groq_client = Groq(api_key=GROQ_API_KEY)

def generate_creative_lines(topics, sentiment_summary, trending_post):
    prompt = f"""
You are a creative strategist writing emotionally resonant social lines for Christmas retail campaigns in New Zealand.
Today's trending topics: {topics}
Sentiment summary: {sentiment_summary}
Sample post: "{trending_post}"

Generate 3 creative lines that emotionally connect with Kiwi shoppers and reflect current retail vibes.
Tone: festive, cheeky, relatable, Kiwi-flavoured
"""
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
