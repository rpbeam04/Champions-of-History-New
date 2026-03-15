import json

import pandas as pd
import wikipediaapi

from .paths import data_path
from .scrape import article_length, scrape_vital_people


def build_participants(scrape_people=False):
    if scrape_people:
        people = scrape_vital_people()
    else:
        with open(data_path("vital_people.json"), "r", encoding="utf-8") as handle:
            people = json.load(handle)

    invitees = pd.read_csv(data_path("invitees.csv"))
    invitees["Level 3"] = False
    json_str = invitees.to_json(orient="records", indent=2).replace("\\/", "/")
    invitee_records = json.loads(json_str)

    with open(data_path("invitees.json"), "w", encoding="utf-8") as handle:
        handle.write(json_str)

    people.extend(invitee_records)
    wiki_wiki = wikipediaapi.Wikipedia(user_agent="HistoryMadness (rpbeam@icloud.com)", language="en")

    for index, person in enumerate(people):
        if index < 3000:
            article_len, summary = article_length(person["Name"], wiki_wiki)
            person["Length"] = article_len
            person["Summary"] = summary
        else:
            person["Length"] = 0
            person["Summary"] = ""

    people = sorted(people, key=lambda item: item["Length"], reverse=True)
    people = sorted(people, key=lambda item: item["Level 3"], reverse=True)

    with open(data_path("participants.json"), "w", encoding="utf-8") as handle:
        json.dump(people, handle, indent=2)

    return people


if __name__ == "__main__":
    build_participants()
