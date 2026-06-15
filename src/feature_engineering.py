import pandas as pd
import numpy as np

df = pd.read_csv(
    "data/processed/master_zomato.csv"
)

# Normalized Votes

df["votes_norm"] = (
    df["votes"] - df["votes"].min()
) / (
    df["votes"].max() - df["votes"].min()
)

# Online Order Feature

df["online_order_num"] = (
    df["online_order"] == "Yes"
).astype(int)

# Table Booking Feature

df["book_table_num"] = (
    df["book_table"] == "Yes"
).astype(int)

# Success Score

df["success_score"] = (
    0.5 * df["rate"].fillna(df["rate"].median())
    +
    0.3 * df["votes_norm"]
    +
    0.1 * df["online_order_num"]
    +
    0.1 * df["book_table_num"]
)

# Save Final Dataset

df.to_csv(
    "data/processed/final_zomato.csv",
    index=False
)

print("Final dataset saved!")