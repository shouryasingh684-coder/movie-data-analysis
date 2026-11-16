import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "archive/tmdb_5000_movies.csv"
os.makedirs("charts", exist_ok = True)

def get_names(text):
    items = json.loads(text)
    return[g["name"] for g in items ]

def load_and_clean(path):
    df = pd.read_csv(path)
    mask = (df["budget"] > 10000) & (df["revenue"] > 0)
    clean = df[mask].copy()
    clean["profit"] = clean["revenue"] - clean["budget"]
    clean["roi"] = clean["profit"] / clean["budget"]
    clean["year"] = pd.to_datetime(clean["release_date"]).dt.year
    clean["genre_list"] = clean["genres"].apply(get_names)
    return clean

def build_tables(clean):
    by_genre = clean.explode("genre_list")
    genre_stats = by_genre.groupby("genre_list")["roi"].agg(["median", "count"])
    big_genre = genre_stats[genre_stats["count"]>= 30]
    mask2 = clean.groupby("year")["roi"].agg(["median","count"])
    by_year = mask2[mask2["count"]>= 20]    
    return big_genre, by_year

def build_charts(clean, big_genre, by_year):
    # chart 1 : median roi by genre
    big_genre = big_genre.sort_values("median", ascending = True)
    fig, ax = plt.subplots(figsize =(8,6))
    ax.barh(big_genre.index, big_genre["median"])  # name then values 
    ax.set_title("Median ROI by genre")
    ax.set_xlabel("Median ROI (profit / budget)")   # stops the label from being cut off
    fig.tight_layout()
    fig.savefig("charts/genre_roi.png")
    plt.close(fig)

    # chart 2: median roi by year
    by_year = by_year.sort_index()
    fig, ax = plt.subplots(figsize =(8,5))
    ax.plot(by_year.index, by_year["median"], marker="o")
    ax.axhline(clean["roi"].median(), linestyle = "--", color ="red", label = "Overall median")
    ax.set_title("Median ROI by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Median ROI (profit / budget)")
    ax.legend()
    fig.tight_layout()
    fig.savefig("charts/roi_by_year.png")
    plt.close(fig)


    roi_small = clean[clean["roi"] < 10]
    

    # chart 4 histogram
    fig, ax = plt.subplots(figsize = (8,5))
    sns.histplot(data = roi_small, x = "roi", bins = 40, ax = ax)
    ax.set_title("Distribution of ROI (movies under 10x)")
    ax.set_xlabel("ROI (profit / budget)")
    ax.set_ylabel("Number of movies")
    fig.tight_layout()
    fig.savefig("charts/roi_hist.png")
    plt.close(fig)

    # chart 5 scatterplot
    fig, ax = plt.subplots(figsize = (6,4))
    sns.scatterplot(data = clean, x = "budget", y = "revenue", alpha = 0.5, ax = ax)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Budget vs Revenue scatterplot")
    ax.set_ylabel("Revenue (log scale)")
    ax.set_xlabel("Budget (log scale)")
    fig.tight_layout()
    fig.savefig("charts/budget_vs_revenue.png")  
    plt.close(fig)

    # chart 6 correlation table
    corr = clean[["budget", "revenue", "popularity", "vote_average", "runtime", "roi"]].corr()
    fig, ax = plt.subplots(figsize =(7,5))
    sns.heatmap(corr, annot = True, fmt = ".2f", cmap = "coolwarm", ax = ax)
    fig.tight_layout()
    fig.savefig("charts/correlations.png")
    plt.close(fig)

clean = load_and_clean(DATA_PATH)
big_genre, by_year = build_tables(clean)
build_charts(clean, big_genre, by_year)
print("Done charts saved in the chart folder.")
