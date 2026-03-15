import json
import math
import random
from collections import Counter
from copy import deepcopy

import pandas as pd

from .paths import data_path
from .utils import generate_seed_order


with open(data_path("participants.json"), "r", encoding="utf-8") as handle:
    participants = json.load(handle)

seed = 0
for index, person in enumerate(participants):
    if index % 32 == 0:
        seed += 1
    person["Seed"] = seed

region_data = pd.read_csv(data_path("regions.csv"))
regions = []
final_32 = {}
for _, row in region_data.iterrows():
    sites = [site.strip() for site in row["First Weekend Sites"].split(";")]
    if row["Region"] != "Final 32":
        region = {
            "Name": row["Region"].strip(),
            "Sites": sites + sites,
            "Final": row["Second Weekend Site"].strip(),
            "Bracket": [[]],
        }
        regions.append(region)
    else:
        final_32 = {
            "Name": row["Region"].strip(),
            "Sites": sites + sites,
            "Final": row["Second Weekend Site"].strip(),
            "Bracket": [[]],
        }


def seed_weight(seed_value, exponent=1.15):
    return 1 / (seed_value ** exponent)


blacklist = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    "f1": ["Erich Ludendorff", "Talaat Pasha", "Albert Speer"],
    "f2": [
        "Heinrich Himmler",
        "Joseph Goebbels",
        "Osama bin Laden",
        "Erwin Rommel",
        "Hermann Göring",
        "Ion Antonescu",
        "Paul von Hindenburg",
        "Ante Pavelić",
    ],
    "f3": ["Adolf Hitler", "Pol Pot", "Benito Mussolini", "Hirohito"],
    "f4": ["Mao Zedong", "Leopold II of Belgium"],
    "f5": ["Joseph Stalin"],
    "f6": [],
}


def choose_winner(p1, p2, round_stage, blacklist_map):
    s1 = p1["Seed"]
    s2 = p2["Seed"]

    if p1["Name"] in blacklist_map.get(round_stage, []) and p2["Name"] in blacklist_map.get(round_stage, []):
        if len(str(round_stage)) > 1:
            next_rd = f"f{int(str(round_stage).strip('f')) + 1}"
        elif round_stage == 6:
            next_rd = "f1"
        else:
            next_rd = round_stage + 1

        winner = p1 if s1 < s2 else p2
        blacklist_map[next_rd].append(winner["Name"])
        return winner

    if p1["Name"] in blacklist_map.get(round_stage, []):
        return p2
    if p2["Name"] in blacklist_map.get(round_stage, []):
        return p1

    if round_stage in [1, 2]:
        exp = 1.12
        if s1 >= 49 or s2 >= 49:
            high_seed = max(s1, s2)
            scale = (high_seed - 49) / (64 - 49)
            exp = 1.12 + scale * (1.25 - 1.12)
        w1 = seed_weight(s1, exponent=exp)
        w2 = seed_weight(s2, exponent=exp)
    elif round_stage in [3, 4]:
        exp = 0.85
        if s1 >= 49 or s2 >= 49:
            high_seed = max(s1, s2)
            scale = (high_seed - 49) / (64 - 49)
            exp = 0.85 + scale * (1 - 0.85)
        w1 = seed_weight(s1, exponent=exp)
        w2 = seed_weight(s2, exponent=exp)
    elif round_stage in [5, 6]:
        base = 6
        w1 = math.log(s2 + base, base)
        w2 = math.log(s1 + base, base)
    elif round_stage in ["f1", "f2", "f3"]:
        base = 9
        w1 = math.log(s2 + base, base)
        w2 = math.log(s1 + base, base)
    else:
        base = 12
        w1 = math.log(s2 + base, base)
        w2 = math.log(s1 + base, base)

    return random.choices([p1, p2], weights=[w1, w2])[0]


def print_stats(region_counts, ct, sims):
    for seed_value in range(1, 9):
        print(f"{seed_value}: {100 * region_counts[seed_value] / (ct * sims):.2f}%")
    print(f"9-16: {100 * sum(region_counts[i] for i in range(9, 17)) / (ct * sims):.2f}%")
    print(f"16+: {100 * sum(region_counts[i] for i in range(17, 65)) / (ct * sims):.2f}%")
    print(f"~Lvl 4: {100 - 100 * sum(region_counts[i] for i in range(1, 5)) / (ct * sims):.2f}%")


def run_simulation(sims=1000):
    regionals = []
    elite8 = []
    winners = []

    for _ in range(sims):
        simulation_regions = deepcopy(regions)
        simulation_final_32 = deepcopy(final_32)
        blacklist_map = deepcopy(blacklist)
        random.shuffle(simulation_regions)

        seed_order = generate_seed_order(64)
        for seed_value in seed_order:
            seed_participants = [p for p in participants if p["Seed"] == seed_value]
            for region in simulation_regions:
                choice = random.choice(seed_participants)
                seed_participants.remove(choice)
                region["Bracket"][0].append(choice)

        for index, region in enumerate(simulation_regions):
            for round_index in range(0, 6):
                simulation_regions[index]["Bracket"].append([])
                matchup_index = 0
                while matchup_index < len(region["Bracket"][round_index]):
                    winner = choose_winner(
                        region["Bracket"][round_index][matchup_index],
                        region["Bracket"][round_index][matchup_index + 1],
                        round_index + 1,
                        blacklist_map,
                    )
                    simulation_regions[index]["Bracket"][round_index + 1].append(winner)
                    matchup_index += 2
            simulation_regions[index]["Winner"] = region["Bracket"][6][0]

        for region in simulation_regions:
            simulation_final_32["Bracket"][0].append(region["Winner"])

        for round_index in range(0, 5):
            simulation_final_32["Bracket"].append([])
            matchup_index = 0
            while matchup_index < len(simulation_final_32["Bracket"][round_index]):
                winner = choose_winner(
                    simulation_final_32["Bracket"][round_index][matchup_index],
                    simulation_final_32["Bracket"][round_index][matchup_index + 1],
                    f"f{round_index + 1}",
                    blacklist_map,
                )
                simulation_final_32["Bracket"][round_index + 1].append(winner)
                matchup_index += 2
        simulation_final_32["Winner"] = simulation_final_32["Bracket"][5][0]

        for region in simulation_regions:
            regionals.append(region["Winner"]["Seed"])
        for person in simulation_final_32["Bracket"][2]:
            elite8.append(person["Seed"])
        winners.append(simulation_final_32["Winner"]["Seed"])

    print("Regions")
    print_stats(Counter(regionals), 32, sims)
    print("Elite 8")
    print_stats(Counter(elite8), 8, sims)
    print("\nWinners")
    print_stats(Counter(winners), 1, sims)


if __name__ == "__main__":
    run_simulation()
