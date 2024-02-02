import pandas as pd

df = pd.read_csv("imdb_top_49_edited.csv")
df["runtime"] = df["runtime"].str.replace(" min","")
df["gross"] = df["gross"].str.replace(",","") 


df.to_csv("test.csv")