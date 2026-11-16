import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("archive/tmdb_5000_movies.csv")
print(df.shape)
print(df.columns)
print(df.head(3))
print(df.isna().sum())
print(len(df[df["budget"]==0]))
print(len(df[df["revenue"]==0]))

mask = (df["budget"] > 10000) & (df["revenue"] > 0)
clean = df[mask].copy()
print(clean.shape)
clean["profit"] = clean["revenue"] - clean["budget"]
clean["roi"] = clean["profit"] / clean["budget"]
print(clean.sort_values("roi", ascending = False).head(5))

print("Mean: ", clean["roi"].mean())
print("Median: ", clean["roi"].median())
clean["year"] = pd.to_datetime(clean["release_date"]).dt.year
print(clean.groupby("year")["title"].count().sort_values(ascending = False).head(5))
print(clean.groupby("year")["roi"].agg(["median", "count"]))

mask2 = clean.groupby("year")["roi"].agg(["median","count"])
by_year = mask2[mask2["count"]>= 20]
print(by_year.sort_values("median", ascending = False))
print(by_year.shape)
print(df["release_date"].max())

def get_names(text):
    items = json.loads(text)
    return[g["name"] for g in items ]

clean["genre_list"] = clean["genres"].apply(get_names)
print(clean[["title", "genre_list"]].head())

by_genre = clean.explode("genre_list")
print(clean.shape)
print(by_genre.shape)

genre_stats = by_genre.groupby("genre_list")["roi"].agg(["median", "count"])
print(genre_stats.sort_values("count"))

big_genre = genre_stats[genre_stats["count"]>= 30]
print(big_genre.sort_values("median", ascending = False))

# chart 1 : median roi by genre
big_genre = big_genre.sort_values("median", ascending = True)
fig, ax = plt.subplots(figsize =(8,6))
ax.barh(big_genre.index, big_genre["median"])  # name then values 
ax.set_title("Median ROI by genre")
ax.set_xlabel("Median ROI (profit / budget)")   # stops the label from being cut off
fig.tight_layout()
fig.savefig("charts/genre_roi.png")
plt.show()

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
plt.show()


roi_small = clean[clean["roi"] < 10]
print(len(clean), len(roi_small))

fig, ax = plt.subplots(figsize = (8,5))
sns.histplot(data = roi_small, x = "roi", bins = 40, ax = ax)
ax.set_title("Distribution of ROI (movies under 10x)")
ax.set_xlabel("ROI (profit / budget)")
ax.set_ylabel("Number of movies")
fig.tight_layout()
fig.savefig("charts/roi_hist.png")
plt.show()

fig, ax = plt.subplots(figsize = (6,4))
sns.scatterplot(data = clean, x = "budget", y = "revenue", alpha = 0.5, ax = ax)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Budget vs Revenue scatterplot")
ax.set_ylabel("Budget (log scale)")
ax.set_xlabel("Budget (log scale)")
fig.tight_layout()
fig.savefig("charts/budget_vs_revenue.png")  
plt.show()

corr = clean[["budget", "revenue", "popularity", "vote_average", "runtime", "roi"]].corr()
fig, ax = plt.subplots(figsize =(7,5))
sns.heatmap(corr, annot = True, fmt = ".2f", cmap = "coolwarm", ax = ax)
fig.tight_layout()
fig.savefig("charts/correlations.png")
plt.show()
