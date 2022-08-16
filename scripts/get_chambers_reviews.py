import json

import pandas as pd
import asyncio
import aiohttp

async def get(id, session):
    try:
        async with session.get(f"https://api.chambers.com/api/individuals/{int(id)}/chambers-reviews") as response:
            try:
                resp = await response.read()
                return json.loads(resp)
            except:
                print('no body for id: ', id)

            # print(type(resp))
            # print(resp)
            # return resp
            # return lawyer
            # if lawyer.status_code != 204:  # if there's no data on this id, just skip
                # print("Successfully got person {} with resp of length {}.".format(row[0], len(lawyer)))
                # lawyer["personOrganisationId"] = row["personOrganisationId"]
                # lawyer["name"] = row["personName"]
                # lawyer["image"] = row["profilePictureUrl"]
                # return lawyer

    except Exception as e:
        print("hit exception: ", e)
        breakpoint()

async def get_chambers_reviews():
    # open data from csv
    df = pd.read_csv("data/aug15-2022/lawyers.csv")
    # results = []

    # ropes & gray = 3650
    # kirkland & ellis = 3636
    # df_org_lawyers = df.query("organisationId == 3636", engine="python")

    org_lawyers = df.drop_duplicates(subset="personOrganisationId").dropna(
        subset="personOrganisationId"
    )
    org_lawyers = org_lawyers.reset_index()

    print("length: ", len(org_lawyers))
    
    # print(type(org_lawyers.values().tolist()))
    # print(org_lawyers.values.tolist())
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[get(row, session) for row in org_lawyers['personOrganisationId'].tolist()]) # just grab first items in list for speed while testing script
    print("Finalized all. Return is a list of len {} outputs.".format(len(results)))
    print('results: ', results)
    
    with open("data/aug15-2022/chambers_reviews.json", "w") as reviewsjson:
        json.dump(results, reviewsjson, indent=4)
        print(f"data dumped into json file")

asyncio.run(get_chambers_reviews())
