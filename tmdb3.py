import pandas as pd
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
