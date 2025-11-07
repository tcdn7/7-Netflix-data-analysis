from enum import unique
from pathlib import Path
from re import split

import pandas as pd

from src.eda import (
    plot_type_distribution,
    plot_content_trend_by_year,
    plot_top_countries,
    plot_top_genres,
    plot_rating_distiribution,
)
from src.insights import (
    yearly_type_trend,
    country_type_heatmap,
    yearly_genre_diversity,
    top_director,
)


def load_cleaned_data() -> pd.DataFrame:
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "netflix_titles_cleaned.csv"

    df = pd.read_csv(data_path)
    print(f"Loaded cleaned dataset from: {data_path}")
    print(f"Shape: {df.shape}")
    return df


def print_high_level_summary(df: pd.DataFrame) -> None:
    total_titles = len(df)
    type_counts = df["type"].value_counts()
    type_ratio = df["type"].value_counts(normalize=True) * 100

    unique_countries = (
        df["country"].dropna().str.split(",").explode().str.strip().nunique()
    )

    unique_genres = (
        df["listed_in"].dropna().str.split(",").explode().str.strip().nunique()
    )

    earliest_year = int(df["release_year"].min())
    latest_year = int(df["release_year"].max())

    print("\n===== NETFLİX DATASET SUMMARY =====")
    print(f"Toral titles: {total_titles}")
    print(f"Time span: {earliest_year} - {latest_year}")
    print(f"Number of unique countries: {unique_countries}")
    print(f"Number of unique genres: {unique_genres}\n")

    print("Conetent type distribution:")
    for t, c in type_counts.items():
        pct = type_ratio[t]
        print(f"  -{t}: {c} titles ({pct:.1f}%)")


def run_visual_report(df: pd.DataFrame) -> None:

    plot_type_distribution(df)
    plot_rating_distiribution(df)

    plot_content_trend_by_year(df)
    yearly_type_trend(df)

    plot_top_countries(df, top_n=10)
    plot_top_genres(df, top_n=10)
    country_type_heatmap(df)

    yearly_genre_diversity(df)
    top_director(df)


def main() -> None:
    df = load_cleaned_data()
    print_high_level_summary(df)
    run_visual_report(df)
    print("\nReport finished. All key figures have been generated.")


if __name__ == "__main__":
    main()
