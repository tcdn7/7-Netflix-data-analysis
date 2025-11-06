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
    cleaned_df = df.copy()

    print("\n===== MISSING VALUES (PERCENTAGE) =====")
    missing_ratio = cleaned_df.isna().mean().sort_values(ascending=False)
    print(missing_ratio)

    fill_unknown_cols = ["director", "cast", "country"]
    for col in fill_unknown_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].fillna("Unknown")

    if "date_added" in cleaned_df.columns:
        before_rows = cleaned_df.shape[0]
        cleaned_df = cleaned_df.dropna(subset=["date_added"])
        after_rows = cleaned_df.shape[0]
        print(f"\nDropped {before_rows - after_rows} rows due to missing 'date_added'.")

    if "date_added" in cleaned_df.columns:
        cleaned_df["date_added"] = pd.to_datetime(
            cleaned_df["date_added"], errors="coerce"
        )

    if "release_year" in cleaned_df.columns:
        cleaned_df["release_year"] = cleaned_df["release_year"].astype(int)

    text_cols = ["type", "country", "rating", "listed_in"]
    for col in text_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.lower().str.strip()

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

        cleaned_df = cleaned_df.drop(columns=["duration_number"])

    print("\n===== CLEANED DATASET INFO =====")
    cleaned_df.info()

    print("\nMissing values after cleaning:")
    print(cleaned_df.isna().sum())

    return cleaned_df


def main() -> None:
    data_path = "data/netflix_titles.csv"

    df = load_dataset(data_path)

    cleaned_df = clean_dataset(df)

    cleaned_df.to_csv("data/netflix_titles_cleaned.csv", index=False)
    print("\nCleaned dataset saved to 'data/netflix_titles_cleaned.csv'.")


if __name__ == "__main__":
    main()
