import json
import string
from time import sleep

import requests

SEARCH_URL = "https://api.chambers.com/api/search/name"
# ORG_PROFILE_URL = "https://api.chambers.com/api/organisations/23254203/profile-basics"
# ORG_PROVIDED_PROFILES_URL = "https://api.chambers.com/api/organisations/23254203/provided-profiles"
# ORG_DEPARTMENTS_URL = "https://api.chambers.com/api/organisations/23254203/ranked-departments"
# ORG_LAWYERS_URL = "https://api.chambers.com/api/organisations/23254203/ranked-lawyers"

SUPPORTED_GUIDES = ["USA"]


# map Description: Id
GUIDE_INFO = {
    "Global": {"id": 2, "description": "Global"},
    "USA": {"id": 5, "description": "USA"},
    "UK": {"id": 1, "description": "UK"},
    "Latin America": {"id": 9, "description": "Latin America"},
    "Asia-Pacific": {"id": 8, "description": "Asia-Pacific"},
    "Greater China Region": {"id": 116, "description": "Greater China Region"},
    "High Net Worth": {"id": 21, "description": "High Net Worth"},
    "FinTech": {"id": 49, "description": "FinTech"},
}


def index_firms():
    """index all of the firm ids (called organization ids) into a file 'firms.json'

    Only index firms from the currently supported guides,
    and save them based on which guide they belong to.

    Response Format:
    {'count': 19667, 'skip': 0, 'take': 5, 'results': [{'facetedSearchId': 11041, 'rowType': 'Firms', 'organisationName': 'Abell Eskew Landau', 'organisationId': 23254203, 'organisationLocation': 'New York', 'town': 'New York', 'country': 'USA', 'profilePictureUrl': 'https://media.chambers.com/organisations/392522/8b600834-87a5-45f3-8ec9-939c440776bb/profile.png', 'hasPaidProfile': True, 'publicationTypeGroups': [{'id': 5, 'description': 'USA'}]}]} # noqa: E501
    """
    PAGE_SIZE = 2000
    # DATA_FILENAME = "firms.json"
    # supported_guide_ids = [GUIDE_INFO[guide]["id"] for guide in SUPPORTED_GUIDES]
    body = {
        "query": "",
        "skip": 0,
        "take": PAGE_SIZE,
        "guideIds": [],
        "locationIds": [],
        "practiceAreaIds": [],
        "entityTypes": [],
    }

    for letter in string.ascii_lowercase[4:]:
        body["query"] = letter  # 'a'

        count = PAGE_SIZE + 9999  # make count larger than PAGE_SIZE
        skip = 0
        results = []

        # next page
        while skip < count:
            sleep(0.2)  # sleep 0.2 seconds
            response = requests.post(SEARCH_URL, json=body)
            data = response.json()
            results += data["results"]
            count = data["count"]
            skip += PAGE_SIZE
            body["skip"] = skip

        with open("bandit/bandit/firms.json", "r") as firmsjson:
            firms = json.load(firmsjson)

        firms.extend(results)

        with open("bandit/bandit/firms.json", "w") as firmsjson:
            json.dump(firms, firmsjson, indent=4)
            print(f"appended the letter {letter}")

        sleep(5)


index_firms()
