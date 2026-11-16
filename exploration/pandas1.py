import pandas as pd
movies = pd.DataFrame({"Title": ["Inception", "Prestige", "Dunkirk", "Digger", "Fightclub"],
                       "Budget": [100, 35, 45, 58, 25],
                       "Revenue": [400, 120, 85, 145, 200],
                       "Rating": [6.0, 9.2, 6.8, 9.3, 9.6],
                       "Genre": ["Action", "Thriller", "War", "Comedy", "Darkcomedy"],
                       })
print(movies.head())
movies.info()
print(movies.describe())
print(movies[['Title', 'Rating']])
print(movies[movies["Rating"]>7])
movies["Profit"] = movies["Revenue"] - movies["Budget"]
print(movies["Profit"])
print(movies.sort_values("Profit", ascending = False))
movies["ROI"] = movies["Profit"] / movies["Budget"]
print(movies["ROI"])
print(movies.sort_values("ROI", ascending = False))

print(movies["Title"])
print(movies[["Title"]])