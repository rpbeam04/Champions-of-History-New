import random
import pandas as pd


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
    import random

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
