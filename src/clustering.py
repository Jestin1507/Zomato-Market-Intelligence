import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/final_zomato.csv"
)

# ==========================================
# LOCATION LEVEL DATA
# ==========================================

location_df = (
    df.groupby("location")
    .agg({
        "rate": "mean",
        "votes": "mean",
        "approx_cost(for two people)": "mean"
    })
    .reset_index()
)

location_df = location_df.dropna()

# ==========================================
# FEATURES
# ==========================================

features = location_df[
    [
        "rate",
        "votes",
        "approx_cost(for two people)"
    ]
]

scaler = StandardScaler()

scaled_features = scaler.fit_transform(
    features
)

# ==========================================
# CLUSTERING
# ==========================================

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

location_df["cluster"] = (
    kmeans.fit_predict(
        scaled_features
    )
)

# ==========================================
# CLUSTER SUMMARY
# ==========================================

print(
    location_df.groupby(
        "cluster"
    ).agg({
        "rate": "mean",
        "votes": "mean",
        "approx_cost(for two people)": "mean"
    })
)

print("\nCluster Locations\n")

print(
    location_df[
        ["location", "cluster"]
    ].sort_values(
        "cluster"
    )
)