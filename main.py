import pandas as pd
import numpy as np


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("==== RAW DATASET INFO =====")
    print(f"Dataset shape: {df.shape}")
    print("\n===== MISSING VALUES =====")
    print(df.isna().sum())
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Netflix dataset."""
    cleaned_df = df.copy()

    if "duration" in cleaned_df.columns and "type" in cleaned_df.columns:
        cleaned_df["duration_number"] = (
            cleaned_df["duration"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .astype(float)
        )

        cleaned_df["duration_minutes"] = np.where(
            cleaned_df["type"] == "movie",
            cleaned_df["duration_number"],
            np.nan,
        )

        cleaned_df["seasons"] = np.where(
            cleaned_df["type"] == "tv show",
            cleaned_df["duration_number"],
            np.nan,
        )

        cleaned_df = cleaned_df.drop(columns=["duration_number"])

    return cleaned_df


def main() -> None:
    data_path = "data/netflix_titles.csv"

    df = load_dataset(data_path)

    cleaned_df = clean_dataset(df)

    cleaned_df.to_csv("data/netflix_titles_cleaned.csv", index=False)
    print("\nCleaned dataset saved to 'data/netflix_titles_cleaned.csv'.")


if __name__ == "__main__":
    main()
