from weasyprint import HTML
import random
import json
import pandas as pd
from pprint import pprint


def generate_seed_order(n):
    seeds = [1, 2]
    while len(seeds) < n:
        m = len(seeds) * 2
        i = 0
        while i < len(seeds):
            if seeds[i] <= m / 2:
                if seeds[i] == 1:
                    seeds.insert(i + 1, m + 1 - seeds[i])
                else:
                    seeds.insert(i, m + 1 - seeds[i])
                i += 1
            i += 1
        if len(seeds) > n / 2:
            i = 0
            while i < len(seeds):
                if seeds[i] > seeds[i + 1]:
                    s = seeds[i]
                    seeds[i] = seeds[i + 1]
                    seeds[i + 1] = s
                i += 2

    return seeds


def generate_full_bracket_html(people, regions):
    def generate_blank_round_ul(round_num, num_matchups):
        html = [f'<ul class="round round-{round_num}">']
        for _ in range(num_matchups):
            location = ""
            if round_num == 3:
                location = random.choice(region["Sites"])
                region["Sites"].remove(location)
            html.append('<li class="spacer"></li>')
            html.append('<li class="game game-top">&nbsp;</li>')
            html.append(f'<li class="game game-spacer">{location}</li>')
            html.append('<li class="game game-bottom">&nbsp;</li>')
        html.append('<li class="spacer"></li>')
        html.append('</ul>')
        return html

    region = random.choice(regions)
    html = [f"<h1>{region['Name']} ({region['Final']})</h1>"]

    html.append('<main>')

    # LEFT BRACKET
    html.append('<div class="bracket-left">')
    html.append('<ul class="round round-1">')

    for i in range(0, 32, 2):
        t1 = people[i]
        t2 = people[i + 1]
        html.append('<li class="spacer"></li>')
        html.append(f'<li class="game game-top"><span class="seed">{t1["Seed"]}</span>{t1["Name"]}</li>')
        html.append('<li class="game game-spacer"></li>')
        html.append(f'<li class="game game-bottom"><span class="seed">{t2["Seed"]}</span>{t2["Name"]}</li>')
        html.append('<li class="spacer"></li>')

    html.append('</ul>')

    matchups = 16
    for r in range(2, 6):
        matchups //= 2
        html.extend(generate_blank_round_ul(r, matchups))

    html.append('<ul class="round round-6">')
    html.append('<li class="spacer"></li>')
    html.append('<li class="game game-top">&nbsp;</li>')
    html.append('<li class="spacer"></li>')
    html.append('</ul>')

    html.append('</div>')  # close .bracket-left

    # CENTER (Champion)
    html.append('<div class="bracket-center">')
    html.append('<ul class="round round-7">')
    html.append('<li class="game game-top">Champion</li>')
    for _ in range(3):
        html.append('<li class="spacer">&nbsp;</li>')
    html.append('</ul>')
    html.append('</div>')

    # RIGHT BRACKET
    html.append('<div class="bracket-right">')
    html.append('<ul class="round round-1">')

    for i in range(32, 64, 2):
        t1 = people[i]
        t2 = people[i + 1]
        html.append('<li class="spacer"></li>')
        html.append(f'<li class="game game-top">{t1["Name"]} <span class="seed">{t1["Seed"]}</span></li>')
        html.append('<li class="game game-spacer"></li>')
        html.append(f'<li class="game game-bottom">{t2["Name"]} <span class="seed">{t2["Seed"]}</span></li>')
        html.append('<li class="spacer"></li>')

    html.append('</ul>')

    matchups = 16
    for r in range(2, 6):
        matchups //= 2
        html.extend(generate_blank_round_ul(r, matchups))

    html.append('<ul class="round round-6">')
    html.append('<li class="spacer"></li>')
    html.append('<li class="game game-top">&nbsp;</li>')
    html.append('<li class="spacer"></li>')
    html.append('</ul>')

    html.append('</div>')  # close .bracket-right
    html.append('</main>')

    return "\n".join(html)


if __name__ == "__main__":
    with open('participants.json', 'r', encoding='utf-8') as f:
        participants = json.load(f)

    seed = 0
    for i, person in enumerate(participants):
        if i % 32 == 0:
            seed += 1
        person["Seed"] = seed

    seeds = generate_seed_order(64)
    people = []
    for s in seeds:
        r = random.randint((s - 1) * 32, s * 32 - 1)
        people.append(participants[r])
        assert participants[r]["Seed"] == s, f"{participants[r]['Seed']} {s}"

    region_data = pd.read_csv('regions.csv')
    regions = []
    for _, row in region_data.iterrows():
        if row["Region"] != "Final 32":
            region = {}
            region["Name"] = row["Region"].strip()
            sites = row["First Weekend Sites"].split(";")
            sites = [site.strip() for site in sites]
            region["Sites"] = sites + sites
            region["Final"] = row["Second Weekend Site"].strip()
            regions.append(region)

    bracket = generate_full_bracket_html(people, regions)

    with open("BracketTop.html", "r", encoding="utf-8") as f:
        bracket_top = f.read()
        bracket_bottom = "</main></body></html>"

    html = bracket_top + bracket + bracket_bottom
    # with open("Bracket.html", "w", encoding="utf-8") as f:
    #     f.write(html)

    HTML(string=html).write_pdf('output.pdf')
