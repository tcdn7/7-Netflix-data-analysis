import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (11, 6)


def yearly_type_trend(df: pd.DataFrame) -> None:
    yearly = (
        df.query("release_year >= 2010")
        .groupby(["release_year", "type"])
        .size()
        .unstack(fill_value=0)
    )

    print("\n===== YEARLY TREND (Movies vs TV Shows) =====")
    print(yearly.tail())

    yearly.plot(kind="line", marker="o")
    plt.title("Yearly Content Trend (2010-2021)")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Titles")
    plt.legend(title="Type")
    plt.show()


def country_type_heatmap(df: pd.DataFrame) -> None:
    """Show top 10 countries by content type using heatmap."""
    if "country" not in df.columns:
        print("No 'country' column found.")
        return

    df_countries = df.dropna(subset=["country"]).copy()

    df_countries["country"] = df_countries["country"].str.split(",")
    df_countries = df_countries.explode("country")
    df_countries["country"] = df_countries["country"].str.strip()

    country_type = (
        df_countries.groupby(["country", "type"]).size().unstack(fill_value=0)
    )

    top10 = country_type.sum(axis=1).sort_values(ascending=False).head(10)
    top10_heatmap = country_type.loc[top10.index]

    print("\n===== TOP 10 COUNTRIES HEATMAP DATA =====")
    print(top10_heatmap)

    sns.heatmap(
        top10_heatmap,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        linewidths=0.5,
    )
    plt.title("Top 10 Countries by Content Type")
    plt.xlabel("Content Type")
    plt.ylabel("Country")
    plt.show()


def yearly_genre_diversity(df: pd.DataFrame) -> None:
    df_genres = df.dropna(subset=["listed_in"]).copy()
    df_genres["listed_in"] = df_genres["listed_in"].str.split(",")
    df_genres = df_genres.explode("listed_in")

    df_genres["listed_in"] = df_genres["listed_in"].astype(str).str.strip().str.lower()

    diversity = (
        df_genres.groupby("release_year")["listed_in"]
        .nunique()
        .reset_index(name="unique_genres")
    )

    print("\n===== YEARLY GENRE DIVERSITY =====")
    print(diversity.tail())

    sns.lineplot(
        data=diversity, x="release_year", y="unique_genres", marker="o", color="tomato"
    )
    plt.title("Genre Diversity by Year")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Unique Genres")
    plt.show()


def top_director(df: pd.DataFrame) -> None:
    directors = df["director"].dropna().value_counts().head(10)

    print("\n===== TOP 10 DIRECTORS =====")
    print(directors)

    sns.barplot(x=directors.values, y=directors.index, palette="magma")
    plt.title("Top 10 Most Prolific Netflix Directors")
    plt.xlabel("Number of Titles")
    plt.ylabel("Director")
    plt.show()


def main() -> None:
    df = pd.read_csv("data/netflix_titles_cleaned.csv")

    yearly_type_trend(df)
    country_type_heatmap(df)
    yearly_genre_diversity(df)
    top_director(df)


if __name__ == "__main__":
    main()
