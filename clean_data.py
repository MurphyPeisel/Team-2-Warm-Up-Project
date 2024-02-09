import pandas as pd

df = pd.read_csv("imdb_top_49_edited.csv")
df["runtime"] = df["runtime"].str.replace(" min","")
df["gross"] = df["gross"].str.replace(",","")
df = df.drop(columns=["certificate"])

df.to_csv("imdb_edited.csv")