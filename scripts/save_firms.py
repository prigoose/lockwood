import pandas as pd

df = pd.read_csv("firms.csv")
df.columns = [c.lower() for c in df.columns]  # PostgreSQL doesn't like capitals or spaces

from sqlalchemy import create_engine

engine = create_engine("postgresql://priyaghose:password@localhost:5432/lockwood")

df.to_sql("firms", engine)
