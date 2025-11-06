import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sympy import rotations

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)


def plot_type_distribution(df: pd.DataFrame) -> None:
    type_counts = df["type"].value_counts()
    print("\n===== TYPE DISTRIBUTION =====")
    print(type_counts)

    plt.figure(figsize=(6, 6))
    type_counts.plot(kind="pie", autopct="%1.1f%%", colors=["#66b3ff", "#99ff99"])
    plt.title("Distribution of Movies vs TV Shows")
    plt.ylabel("")
    plt.show()


def plot_content_trend_by_year(df: pd.DataFrame) -> None:
    yearly_counts = df.groupby("release_year").size().reset_index(name="count")
    yearly_counts = yearly_counts[yearly_counts["release_year"] >= 2010]

    print("\n===== CONTENT TREND SINCE 2010 =====")
    print(yearly_counts.tail())

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=yearly_counts, x="release_year", y="count", marker="o")
    plt.title("Number of Netflix Contents Released Each Year (2010+)")
    plt.xlabel("Released Year")
    plt.ylabel("Number of Contents")
    plt.show()


def plot_top_countries(df: pd.DataFrame, top_n: int = 10) -> None:
    if "country" not in df.columns:
        print("No 'country' column found.")
        return

    countries = df["country"].dropna().str.split(",")
    exploded = countries.explode().str.strip()
    top_countries = exploded.value_counts().head(top_n)

    print("\n===== TOP COUNTRIES =====")
    print(top_countries)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="viridis")
    plt.title(f"Top {top_n} Countries by Number of Netflix Titles")
    plt.xlabel("Number of Titles")
    plt.ylabel("Country")
    plt.show()


def plot_top_genres(df: pd.DataFrame, top_n: int = 10) -> None:
    genres = df["listed_in"].dropna().str.strip(",")
    exploded = genres.explode().str.strip().str.lower()
    top_genres = exploded.value_counts().head(top_n)

    print("\n===== TOP GENRES =====")
    print(top_genres)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_genres.values, y=top_genres.index, palette="coolwarm")
    plt.title(f"Top {top_n} Genres on Netflix")
    plt.xlabel("Number of Titles")
    plt.ylabel("Genre")
    plt.show()


def plot_rating_distiribution(df: pd.DataFrame) -> None:
    rating_counts = df["rating"].value_counts().sort_values(ascending=False)

    print("\n===== RATING DISTRIBUTION =====")
    print(rating_counts)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=rating_counts.index, y=rating_counts.values, palette="mako")
    plt.title("Distribution of Netflix Content Rating")
    plt.xlabel("Rating")
    plt.ylabel("Number of Titles")
    plt.xticks(rotation=45)
    plt.show()


def main() -> None:
    df = pd.read_csv("data/netflix_titles_cleaned.csv")

    plot_type_distribution(df)
    plot_content_trend_by_year(df)
    plot_top_countries(df)
    plot_top_genres(df)
    plot_rating_distiribution(df)


if __name__ == "__main__":
    main()
