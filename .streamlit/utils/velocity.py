def detect_velocity(df_today, df_yesterday):
    today_counts = df_today["hashtags"].explode().value_counts()
    yesterday_counts = df_yesterday["hashtags"].explode().value_counts()
    velocity = (today_counts - yesterday_counts).fillna(0) / yesterday_counts.replace(0, 1)
    return velocity.sort_values(ascending=False).head(10)

def summarize_trends(df_today, df_yesterday):
    new_topics = set(df_today["hashtags"].explode()) - set(df_yesterday["hashtags"].explode())
    return f"New trending topics today: {', '.join(new_topics)}"
