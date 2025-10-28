import streamlit as st
import pandas as pd
from config import GROQ_API_KEY, GROQ_MODEL
from utils.data.static_data import df_today
from utils.clustering import cluster_keywords
from utils.scoring import score_christmas_vibes
from utils.generation import generate_creative_lines
from groq import Groq

groq_client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="NZ Christmas Retail Trend Listener", layout="wide")
st.title("🎄 NZ Christmas Retail Trend Listener + Creative Generator")

# Process data
df_today["cluster"] = cluster_keywords(df_today["post_text"])
df_today["vibe_score"] = df_today["post_text"].apply(score_christmas_vibes)
df_today["sentiment_binary"] = df_today["sentiment"].apply(lambda x: 1 if x == "positive" else 0)
df_yesterday = df_today.sample(frac=0.6, random_state=42)

# Display insights
st.subheader("📊 Trend Insights")
st.dataframe(df_today, use_container_width=True)

# Top hashtags and sentiment
top_hashtags = df_today["hashtags"].explode().value_counts().head(5).index.tolist()
top_post = df_today.sort_values("engagement", ascending=False).iloc[0]["post_text"]
sentiment_counts = df_today["sentiment_binary"].value_counts().sort_index().to_dict()
sentiment_counts = {0: sentiment_counts.get(0, 0), 1: sentiment_counts.get(1, 0)}

col1, col2, col3 = st.columns(3)
col1.metric("🎯 Top Hashtags", ", ".join([f"#{tag}" for tag in top_hashtags]))
col2.metric("💬 Sentiment (1=pos, 0=neg)", f"{sentiment_counts}")
col3.metric("🎄 Avg Vibe Score", f"{df_today['vibe_score'].mean():.2f}")

# Pre-baked summary
st.markdown("---")
st.subheader("🧵 Pre-Baked Trend Summary")

st.markdown("""
**Top Hashtags:**  
`#giftguide2025`, `#kiwichristmas`, `#bbqseason`, `#nzpost`, `#stockingstuffers`  
These reflect strong engagement around local gifting, delivery logistics, and seasonal outdoor culture.

**What’s Picking Up:**  
- More posts about BBQ kits, pōhutukawa shade, and backyard setups  
- NZ Post tagged in delivery countdowns and rural shipping stress  
- Whānau-focused gifting — “gifts for Mum”, “tamariki surprises”, “family-first Christmas”

**What’s Dropping Off:**  
- Less buzz around global luxury brands  
- Northern Hemisphere tropes (snow, reindeer) fading in favor of beach, BBQ, and native flora
""")

# Pre-baked creative ideas
st.markdown("---")
st.subheader("✨ Pre-Baked Creative Ideas")

st.markdown("""
These lines reflect current sentiment — a mix of excitement, stress, and Kiwi practicality:

- ✅ *“Christmas magic? Nah, it’s just you panic-buying candles and hoping NZ Post delivers on time.”*  
- ✅ *“BBQ smoke, pōhutukawa shade, and a gift that actually lands — now that’s a win.”*  
- ✅ *“She said ‘no fuss this year’ — so you bought her a spa voucher and cried in the carpark.”*  
- ✅ *“Stocking stuffers under $20 that won’t make you look like you forgot — even if you did.”*  
- ✅ *“Grill kits, gift cards, and a dash of emotional damage — your Christmas sorted.”*

**Tone:** Sassy, emotionally grounded, and campaign-ready. Designed for shoppers juggling joy, guilt, and logistics.
""")

# Live creative generation
st.markdown("---")
st.subheader("📝 Creative Lines")
if st.button("Generate"):
    lines = generate_creative_lines(top_hashtags, sentiment_counts, top_post)
    st.markdown("#### ✨ Generated Lines")
    for line in lines.split("\n"):
        if line.strip():
            st.markdown(f"✅ {line.strip()}")

# Chat interface
st.markdown("---")
st.subheader("💬 Chat with the Trend Engine")
user_input = st.chat_input("Ask about NZ Christmas trends or generate a post...")
if user_input:
    chat_prompt = f"""
You are a Christmas retail trend assistant focused on New Zealand audiences.

Your role is to interpret real-time social and search data related to Christmas retail — including trending hashtags, posts, sentiment, and engagement — and respond with either:
- Actionable insights about emerging trends, shopper sentiment, or retail behavior
- Creative, emotionally resonant social lines tailored to Kiwi shoppers

User input: {user_input}

Use today's data to respond with either:
- A concise insight summary (e.g., top hashtags, sentiment shifts)
- Or 2–3 creative lines that reflect current retail vibes in New Zealand

Tone: festive, cheeky, relatable, Kiwi-flavoured. Prioritise cultural relevance, emotional resonance, and campaign utility.
"""
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": chat_prompt}]
    )
    st.chat_message("assistant").markdown(response.choices[0].message.content)
