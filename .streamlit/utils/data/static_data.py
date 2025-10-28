import pandas as pd

data = [
    {
        "platform": "TikTok",
        "post_text": "Farmers just dropped 60% off — is it too early to panic? #BoxingDayNZ #KiwiChristmas",
        "hashtags": ["BoxingDayNZ", "KiwiChristmas"],
        "mentions": ["@FarmersNZ"],
        "engagement": 4200,
        "sentiment": "Positive",
    },
    {
        "platform": "Instagram",
        "post_text": "NZ Post delays again. Gifts might arrive in 2026. #NZPostDelays #ChristmasStress",
        "hashtags": ["NZPostDelays", "ChristmasStress"],
        "mentions": ["@NZPost"],
        "engagement": 3100,
        "sentiment": "Negative",
    },
    {
        "platform": "Twitter",
        "post_text": "Gift ideas for mum that don’t scream ‘last minute’ #GiftIdeasNZ #KiwiChristmas",
        "hashtags": ["GiftIdeasNZ", "KiwiChristmas"],
        "mentions": [],
        "engagement": 1800,
        "sentiment": "Positive",
    },
    {
        "platform": "Google Trends",
        "post_text": "Search spike: ‘Click & collect NZ’ + ‘Boxing Day deals’",
        "hashtags": ["ClickAndCollectNZ", "BoxingDayDeals"],
        "mentions": [],
        "engagement": 2500,
        "sentiment": "Neutral",
    },
]

df_today = pd.DataFrame(data)
