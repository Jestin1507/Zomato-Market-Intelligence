import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)


def clean_zomato_data():

    df = pd.read_csv(
        "data/raw/zomato.csv"
    )

    print("Original Shape:", df.shape)

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean ratings
    df["rate"] = df["rate"].replace(
        ["NEW", "-"],
        np.nan
    )

    df["rate"] = (
        df["rate"]
        .astype(str)
        .str.replace("/5", "", regex=False)
    )

    df["rate"] = pd.to_numeric(
        df["rate"],
        errors="coerce"
    )

    # Clean cost column
    df["approx_cost(for two people)"] = (
        df["approx_cost(for two people)"]
        .astype(str)
        .str.replace(",", "")
    )

    df["approx_cost(for two people)"] = pd.to_numeric(
        df["approx_cost(for two people)"],
        errors="coerce"
    )

    # Save cleaned dataset
    df.to_csv(
        "data/processed/cleaned_zomato.csv",
        index=False
    )

    print("Cleaned dataset saved!")

    # Analysis dataset
    analysis_df = df.copy()

    analysis_df = analysis_df.dropna(
        subset=[
            "location",
            "cuisines",
            "approx_cost(for two people)"
        ]
    )

    analysis_df["rest_type"] = (
        analysis_df["rest_type"]
        .fillna("Unknown")
    )

    analysis_df.to_csv(
        "data/processed/analysis_zomato.csv",
        index=False
    )

    print("Analysis dataset saved!")

    # Master dataset
    master_df = analysis_df.copy()

    master_df = master_df.drop_duplicates(
        subset=["name", "address"]
    )

    master_df.to_csv(
        "data/processed/master_zomato.csv",
        index=False
    )

    print("Master dataset saved!")

    return master_df


if __name__ == "__main__":
    clean_zomato_data()