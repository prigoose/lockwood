import json

import pandas as pd
import requests
import asyncio
import aiohttp
import time

async def get(row, session):
    print(type(row))
    print('row: ', row)
    try:
        response = session.get(
            f"https://api.chambers.com/api/individuals/{int(row['personOrganisationId'])}/chambers-reviews"
        )
        review = await response.read()
        if response.status_code != 204:  # if there's no data on this id, just skip
            # lawyers = response.json()
            print("Successfully got person {} with resp of length {}.".format(row["personName"], len(review)))
            for lawyer in lawyers:
                lawyer["personOrganisationId"] = row["personOrganisationId"]
                lawyer["name"] = row["personName"]
                lawyer["image"] = row["profilePictureUrl"]
            results += lawyers

    except Exception as e:
        print("hit exception: ", e)
        breakpoint()

async def get_chambers_reviews():
    # open data from csv
    df = pd.read_csv("data/aug15-2022/lawyers.csv")
    results = []

    # ropes & gray = 3650
    # kirkland & ellis = 3636
    # df_org_lawyers = df.query("organisationId == 3636", engine="python")

    org_lawyers = df.drop_duplicates(subset="personOrganisationId").dropna(
        subset="personOrganisationId"
    )
    org_lawyers = org_lawyers.reset_index()

    print("length: ", len(org_lawyers))
    
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(row, session) for row in org_lawyers.iterrows()])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))
    
    with open("data/aug15-2022/chambers_reviews.json", "w") as reviewsjson:
        json.dump(results, reviewsjson, indent=4)
        print(f"data dumped into json file")

asyncio.run(get_chambers_reviews())
