import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/final_zomato.csv"
)

# ==========================================
# MODEL DATASET
# ==========================================

model_df = df[
    [
        "rate",
        "votes",
        "approx_cost(for two people)",
        "online_order_num",
        "book_table_num",
        "location",
        "rest_type",
        "listed_in(type)",
        "listed_in(city)",
        "cuisines"
    ]
].copy()

model_df.dropna(inplace=True)

# ==========================================
# FEATURE ENGINEERING
# ==========================================

model_df["cuisine_count"] = (
    model_df["cuisines"]
    .apply(lambda x: len(str(x).split(",")))
)

rest_popularity = (
    model_df
    .groupby("rest_type")["votes"]
    .mean()
)

model_df["rest_popularity"] = (
    model_df["rest_type"]
    .map(rest_popularity)
)

# ==========================================
# LABEL ENCODING
# ==========================================

le_location = LabelEncoder()
le_rest = LabelEncoder()
le_type = LabelEncoder()
le_city = LabelEncoder()

model_df["location_encoded"] = (
    le_location.fit_transform(
        model_df["location"]
    )
)

model_df["rest_type_encoded"] = (
    le_rest.fit_transform(
        model_df["rest_type"]
    )
)

model_df["listed_type_encoded"] = (
    le_type.fit_transform(
        model_df["listed_in(type)"]
    )
)

model_df["listed_city_encoded"] = (
    le_city.fit_transform(
        model_df["listed_in(city)"]
    )
)

# ==========================================
# FEATURES
# ==========================================

features = [
    "votes",
    "approx_cost(for two people)",
    "online_order_num",
    "book_table_num",
    "location_encoded",
    "rest_type_encoded",
    "listed_type_encoded",
    "listed_city_encoded",
    "cuisine_count",
    "rest_popularity"
]

X = model_df[features]
y = model_df["rate"]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# MODEL TRAINING
# ==========================================

rf = RandomForestRegressor(
    n_estimators=500,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf.fit(
    X_train,
    y_train
)

# ==========================================
# EVALUATION
# ==========================================

y_pred = rf.predict(X_test)

print(
    "MAE:",
    round(
        mean_absolute_error(
            y_test,
            y_pred
        ),
        4
    )
)

print(
    "RMSE:",
    round(
        np.sqrt(
            mean_squared_error(
                y_test,
                y_pred
            )
        ),
        4
    )
)

print(
    "R2 Score:",
    round(
        r2_score(
            y_test,
            y_pred
        ),
        4
    )
)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    rf,
    "models/rating_model.pkl"
)

print("Model Saved Successfully")