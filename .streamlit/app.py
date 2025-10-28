import streamlit as st
import pandas as pd
from config import GROQ_API_KEY, GROQ_MODEL
from data.static_data import df_today
from utils.clustering import cluster_keywords
from utils.scoring import score_christmas_vibes
from utils.velocity import detect_velocity, summarize_trends
from utils.generation import generate_creative_lines

st.set_page_config(page_title="NZ Christmas Retail Trend Listener", layout="wide")
st.title("🎄 NZ Christmas Retail Trend Listener + Creative Generator")

# Process data
df_today["cluster"] = cluster_keywords(df_today["post_text"])
df_today["vibe_score"] = df_today["post_text"].apply(score_christmas_vibes)
df_yesterday = df_today.sample(frac=0.6, random_state=42)

# Display insights
st.subheader("📊 Trend Insights")
with st.expander("🔍 View Raw Trend Data"):
    st.dataframe(df_today)

top_hashtags = df_today["hashtags"].explode().value_counts().head(5).index.tolist()
top_post = df_today.sort_values("engagement", ascending=False).iloc[0]["post_text"]
sentiment_summary = df_today["sentiment"].value_counts().to_dict()
velocity_trends = detect_velocity(df_today, df_yesterday)
new_topic_summary = summarize_trends(df_today, df_yesterday)

col1, col2, col3 = st.columns(3)
col1.metric("🎯 Top Hashtags", ", ".join(top_hashtags))
col2.metric("💬 Sentiment", str(sentiment_summary))
col3.metric("🎄 Avg Vibe Score", f"{df_today['vibe_score'].mean():.2f}")

st.markdown("---")
st.subheader("🔥 Velocity-Based Hot Trends")
st.dataframe(velocity_trends)

st.markdown("---")
st.subheader("📝 Creative Lines")
if st.button("Generate"):
    lines = generate_creative_lines(top_hashtags, sentiment_summary, top_post)
    st.markdown(lines)

st.subheader("💬 Chat with the Trend Engine")
user_input = st.chat_input("Ask about NZ Christmas trends or generate a post...")
if user_input:
    from openai import ChatCompletion
    chat_prompt = f"""
You are a Christmas retail trend assistant focused on New Zealand audiences.

Your role is to interpret real-time social and search data related to Christmas retail — including trending hashtags, posts, sentiment, and engagement — and respond with either:
- Actionable insights about emerging trends, shopper sentiment, or retail behavior
- Creative, emotionally resonant social lines tailored to Kiwi shoppers

User input: {user_input}

Use today's data to respond with either:
- A concise insight summary (e.g., top hashtags, sentiment shifts, trend velocity)
- Or 2–3 creative lines that reflect current retail vibes in New Zealand

Tone: festive, cheeky, relatable, Kiwi-flavoured. Prioritise cultural relevance, emotional resonance, and campaign utility.

"""
    chat_response = ChatCompletion.create(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        messages=[{"role": "user", "content": chat_prompt}]
    )
    st.chat_message("assistant").markdown(chat_response["choices"][0]["message"]["content"])
