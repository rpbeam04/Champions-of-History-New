import json
from collections import defaultdict

import pandas as pd

from .paths import data_path
from .utils import generate_full_bracket_html, generate_seed_order


def load_participants():
    with open(data_path("participants.json"), "r", encoding="utf-8") as handle:
        return json.load(handle)


def seed_participants(participants):
    seeded_participants = []
    seed = 0
    for index, person in enumerate(participants):
        participant = dict(person)
        if index % 32 == 0:
            seed += 1
        participant["Seed"] = seed
        seeded_participants.append(participant)
    return seeded_participants


def load_regions(include_final_32=False):
    region_data = pd.read_csv(data_path("regions.csv"))
    regions = []
    for _, row in region_data.iterrows():
        is_final_32 = row["Region"] == "Final 32"
        if is_final_32 and not include_final_32:
            continue
        sites = [site.strip() for site in row["First Weekend Sites"].split(";")]
        regions.append(
            {
                "Name": row["Region"].strip(),
                "Sites": sites + sites,
                "Final": row["Second Weekend Site"].strip(),
            }
        )
    return regions


def build_preview_people(participants):
    people_by_seed = defaultdict(list)
    for person in participants:
        people_by_seed[person["Seed"]].append(person)

    return [people_by_seed[seed][0] for seed in generate_seed_order(64)]


def build_bracket_preview():
    participants = seed_participants(load_participants())
    regions = load_regions()
    people = build_preview_people(participants)
    return generate_full_bracket_html(people, regions)