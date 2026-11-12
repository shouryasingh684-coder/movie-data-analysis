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


