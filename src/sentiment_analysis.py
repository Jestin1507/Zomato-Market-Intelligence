import pandas as pd
import numpy as np

from textblob import TextBlob

import plotly.express as px
import plotly.io as pio

pd.set_option("display.max_columns", None)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/final_zomato.csv"
)

# ==========================================
# CLEAN REVIEWS
# ==========================================

df["reviews_clean"] = (
    df["reviews_list"]
    .astype(str)
    .str.lower()
)

# ==========================================
# SENTIMENT FUNCTION
# ==========================================

def get_sentiment(text):

    polarity = TextBlob(
        text
    ).sentiment.polarity

    if polarity > 0:
        return "Positive"

    elif polarity < 0:
        return "Negative"

    else:
        return "Neutral"

# ==========================================
# SAMPLE DATA
# ==========================================

sample_df = df.sample(
    5000,
    random_state=42
).copy()

sample_df["sentiment"] = (
    sample_df["reviews_clean"]
    .apply(get_sentiment)
)

print(
    sample_df["sentiment"]
    .value_counts()
)

# ==========================================
# VISUALIZATION
# ==========================================

fig = px.pie(
    sample_df,
    names="sentiment",
    title="Review Sentiment Distribution"
)

pio.renderers.default = "browser"

fig.show()