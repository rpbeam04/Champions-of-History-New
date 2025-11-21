import json
import math
import random
from collections import Counter
import pandas as pd
from pathlib import Path
from src.utils import generate_seed_order

# Resolve data/template paths relative to repo root so code works after reorg.
BASE_DIR = Path(__file__).resolve().parents[1]

def data_path(name):
    p = BASE_DIR / 'data' / name
    if p.exists():
        return p
    p = BASE_DIR / name
    return p

# Participants
with open(data_path('participants.json'), 'r', encoding='utf-8') as f:
    participants = json.load(f)

# Seeds
seed = 0
for i, person in enumerate(participants):
    if i % 32 == 0:
        seed += 1
    person['Seed'] = seed

region_data = pd.read_csv(data_path('regions.csv'))
regions = []
final_32 = {}
for _, row in region_data.iterrows():
    if row['Region'] != 'Final 32':
        region = {}
        region['Name'] = row['Region'].strip()
        sites = row['First Weekend Sites'].split(';')
        sites = [site.strip() for site in sites]
        region['Sites'] = sites + sites
        region['Final'] = row['Second Weekend Site'].strip()
        region['Bracket'] = [[]]
        regions.append(region)
    else:
        final_32['Name'] = row['Region'].strip()
        sites = row['First Weekend Sites'].split(';')
        sites = [site.strip() for site in sites]
        final_32['Sites'] = sites + sites
        final_32['Final'] = row['Second Weekend Site'].strip()
        final_32['Bracket'] = [[]]


def seed_weight(seed, exponent=1.15):
    return 1 / (seed ** exponent)


# Blacklist kept as in original; unchanged logic
blacklist = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [],
             'f1': ['Erich Ludendorff','Talaat Pasha','Albert Speer'],
             'f2': ['Heinrich Himmler','Joseph Goebbels','Osama bin Laden','Erwin Rommel',
                    'Hermann Göring','Ion Antonescu','Paul von Hindenburg','Ante Pavelić'],
             'f3': ['Adolf Hitler','Pol Pot','Benito Mussolini','Hirohito'],
             'f4': ['Mao Zedong','Leopold II of Belgium'], 'f5': ['Joseph Stalin'], 'f6': []}


def choose_winner(p1, p2, round_stage):
    s1 = p1['Seed']
    s2 = p2['Seed']

    if p1['Name'] in blacklist.get(round_stage, []) and p2['Name'] in blacklist.get(round_stage, []):
        if len(str(round_stage)) > 1:
            next_rd = f"f{int(str(round_stage).strip('f'))+1}"
        else:
            if round_stage == 6:
                next_rd = 'f1'
            else:
                next_rd = round_stage + 1
        if s1 < s2:
            blacklist[next_rd].append(p1)
            return p1
        else:
            blacklist[next_rd].append(p2)
            return p2
    elif p1['Name'] in blacklist.get(round_stage, []):
        return p2
    elif p2['Name'] in blacklist.get(round_stage, []):
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
    elif round_stage in ['f1', 'f2', 'f3']:
        base = 9
        w1 = math.log(s2 + base, base)
        w2 = math.log(s1 + base, base)
    else:
        base = 12
        w1 = math.log(s2 + base, base)
        w2 = math.log(s1 + base, base)

    return random.choices([p1, p2], weights=[w1, w2])[0]


def print_stats(regions, ct, sims):
    for s in range(1, 9):
        print(f"{s}: {100*regions[s]/(ct*sims):.2f}%")
    print(f"9-16: {100*sum([regions[i] for i in range(9,17)])/(ct*sims):.2f}%")
    print(f"16+: {100*sum([regions[i] for i in range(17,65)])/(ct*sims):.2f}%")
    print(f"~Lvl 4: {100 - 100*sum([regions[i] for i in range(1,5)])/(ct*sims):.2f}%")


def run_simulation(sims=1000):
    regionals = []
    elite8 = []
    winners = []

    for _ in range(sims):
        random.shuffle(regions)

        # Filling in the brackets
        seed_order = generate_seed_order(64)
        for seed in seed_order:
            seed_participants = [p for p in participants if p['Seed'] == seed]
            for region in regions:
                choice = random.choice(seed_participants)
                seed_participants.remove(choice)
                region['Bracket'][0].append(choice)

        # Simulating the regions
        for i, region in enumerate(regions):
            for r in range(0, 6):
                regions[i]['Bracket'].append([])
                j = 0
                while j < len(region['Bracket'][r]):
                    winner = choose_winner(region['Bracket'][r][j], region['Bracket'][r][j+1], r+1)
                    regions[i]['Bracket'][r+1].append(winner)
                    j += 2
            regions[i]['Winner'] = region['Bracket'][6][0]

        # Simulating the final 32
        for region in regions:
            final_32['Bracket'][0].append(region['Winner'])

        for r in range(0, 5):
            final_32['Bracket'].append([])
            j = 0
            while j < len(final_32['Bracket'][r]):
                winner = choose_winner(final_32['Bracket'][r][j], final_32['Bracket'][r][j+1], f"f{r+1}")
                final_32['Bracket'][r+1].append(winner)
                j += 2
        final_32['Winner'] = final_32['Bracket'][5][0]

        for r in regions:
            regionals.append(r['Winner']['Seed'])
        for p in final_32['Bracket'][2]:
            elite8.append(p['Seed'])
        winners.append(final_32['Winner']['Seed'])

        # Reset brackets
        final_32['Bracket'] = [[]]
        for i, region in enumerate(regions):
            regions[i]['Bracket'] = [[]]

    print("Regions")
    regions_ct = Counter(regionals)
    print_stats(regions_ct, 32, sims)
    print("Elite 8")
    elite = Counter(elite8)
    print_stats(elite, 8, sims)
    print("\nWinners")
    win = Counter(winners)
    print_stats(win, 1, sims)


if __name__ == '__main__':
    run_simulation()
