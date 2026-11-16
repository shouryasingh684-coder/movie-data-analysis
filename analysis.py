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