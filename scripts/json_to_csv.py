import pandas as pd

df = pd.read_json("bandit/bandit/firms.json")
df.to_csv("firms.csv")
