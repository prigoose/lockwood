import json

import pandas as pd
from sqlalchemy import create_engine

file = open("bandit/bandit/firms.json")
data = json.load(file)
df = pd.json_normalize(
    data,
    record_path=["publicationTypeGroups"],
    meta=[
        "facetedSearchId",
        "rowType",
        "organisationName",
        "organisationId",
        "organisationLocation",
        "town",
        "country",
        "profilePictureUrl",
        "hasPaidProfile",
        "personOrganisationId",
        "personName",
    ],
    errors="ignore",
)

# df["publicationTypeGroups"] = df["publicationTypeGroups"].apply(json.dumps)

df.to_csv("firms_clean.csv")

# database = create_engine("postgresql://priyaghose:password@localhost:5432/lockwood")

# df.to_sql("firms_new", database)
