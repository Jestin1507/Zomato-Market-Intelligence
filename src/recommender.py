import pandas as pd

df = pd.read_csv(
    "data/processed/final_zomato.csv"
)


def recommend_locations(
    cuisine,
    budget
):

    temp = df.copy()

    temp = temp[
        temp["cuisines"]
        .str.contains(
            cuisine,
            case=False,
            na=False
        )
    ]

    temp = temp[
        temp["approx_cost(for two people)"]
        <= budget
    ]

    result = (
        temp.groupby("location")
        .agg({
            "rate": "mean",
            "votes": "mean",
            "success_score": "mean"
        })
        .reset_index()
    )

    result["score"] = (
        result["success_score"] * 0.8
        +
        (
            result["votes"]
            / result["votes"].max()
        ) * 0.2
    )

    result = result.sort_values(
        "score",
        ascending=False
    )

    return result.head(10)


# Test Example
print(
    recommend_locations(
        cuisine="Italian",
        budget=1000
    )
)

# User Input
cuisine = input("Enter Cuisine: ")
budget = int(input("Enter Budget: "))

recommendations = recommend_locations(
    cuisine,
    budget
)

print("\nTop Recommended Locations:\n")
print(recommendations)

recommendations.to_csv(
    "data/processed/location_recommendations.csv",
    index=False
)

print(
    "\nRecommendations saved to: data/processed/location_recommendations.csv"
)