import json

import pandas as pd
import requests


def get_chambers_reviews():
    # open data from csv
    df = pd.read_csv("data/people.csv")
    results = []

    # ropes & gray = 3650
    # kirkland & ellis = 3636
    df_org_lawyers = df.query("organisationId == 3636", engine="python")

    org_lawyers = df_org_lawyers.drop_duplicates(subset="personOrganisationId").dropna(
        subset="personOrganisationId"
    )
    org_lawyers = org_lawyers.reset_index()

    print("length: ", len(org_lawyers))
    for index, row in org_lawyers.iterrows():
        try:
            print("index: ", index)
            response = requests.get(
                f"https://api.chambers.com/api/individuals/{int(row['personOrganisationId'])}/chambers-reviews"
            )
            if response.status_code == 204:  # if there's no data on this id, just skip
                continue
            lawyers = response.json()
            for lawyer in lawyers:
                lawyer["personOrganisationId"] = row["personOrganisationId"]
                lawyer["name"] = row["personName"]
                lawyer["image"] = row["profilePictureUrl"]
            results += lawyers

        except Exception as e:
            print("hit exception: ", e)
            breakpoint()

    with open("data/chambers_reviews_kirkland_ellis.json", "w") as reviewsjson:
        json.dump(results, reviewsjson, indent=4)
        print(f"data dumped into json file")


get_chambers_reviews()
