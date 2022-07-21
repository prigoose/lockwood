import json

import numpy as np
import pandas as pd
import requests


def get_chambers_reviews():
    # open data from csv
    df = pd.read_csv(r"firms_clean.csv")
    results = []

    df_rg_lawyers = df.query("organisationId == 3650", engine="python")

    # rg_lawyers = df_rg_lawyers.personOrganisationId.dropna().unique()

    # all_lawyers = df.personOrganisationId.dropna().unique()
    rg_lawyers = df_rg_lawyers.drop_duplicates(subset="personOrganisationId").dropna(
        subset="personOrganisationId"
    )
    rg_lawyers = rg_lawyers.reset_index()

    print("length: ", len(rg_lawyers))
    # for index, id in np.ndenumerate(rg_lawyers):
    for index, row in rg_lawyers.iterrows():
        try:
            print("index: ", index)
            response = requests.get(
                f"https://api.chambers.com/api/individuals/{int(row['personOrganisationId'])}/chambers-reviews"
            )
            if response.status_code == 204:  # if there's no data on this id, just skip
                continue
            lawyer = response.json()
            lawyer[0]["name"] = row["personName"]
            lawyer[0]["image"] = row["profilePictureUrl"]
            results += lawyer

        except Exception as e:
            print("hit exception: ", e)
            breakpoint()

    with open("bandit/bandit/chambers_reviews_rg.json", "w") as reviewsjson:
        json.dump(results, reviewsjson, indent=4)
        print(f"data dumped into json file")


get_chambers_reviews()
