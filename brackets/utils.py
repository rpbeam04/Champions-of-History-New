import random


def generate_seed_order(n):
    if n < 2 or n & (n - 1):
        raise ValueError("n must be a power of two greater than 1")

    seeds = [1, 2]
    while len(seeds) < n:
        bracket_size = len(seeds) * 2 + 1
        next_round = []
        for seed in seeds:
            next_round.extend([seed, bracket_size - seed])
        seeds = next_round

    return seeds


def generate_full_bracket_html(people, regions):
    region = random.choice(regions)
    site_pool = list(region.get("Sites", []))

    def person_name(person):
        return person.get("Name", f"Seed {person['Seed']}")

    def next_site():
        if not site_pool:
            return ""
        return site_pool.pop(random.randrange(len(site_pool)))

    def generate_blank_round_ul(round_num, num_matchups):
        html = [f'<ul class="round round-{round_num}">']
        for _ in range(num_matchups):
            location = ""
            if round_num == 3:
                location = next_site()
            html.append('<li class="spacer"></li>')
            html.append('<li class="game game-top">&nbsp;</li>')
            html.append(f'<li class="game game-spacer">{location}</li>')
            html.append('<li class="game game-bottom">&nbsp;</li>')
        html.append('<li class="spacer"></li>')
        html.append('</ul>')
        return html

    html = [f"<h1>{region['Name']} ({region['Final']})</h1>"]

    html.append('<main>')

    # LEFT BRACKET
    html.append('<div class="bracket-left">')
    html.append('<ul class="round round-1">')

    for i in range(0, 32, 2):
        t1 = people[i]
        t2 = people[i + 1]
        html.append('<li class="spacer"></li>')
        html.append(f'<li class="game game-top"><span class="seed">{t1["Seed"]}</span>{person_name(t1)}</li>')
        html.append('<li class="game game-spacer"></li>')
        html.append(f'<li class="game game-bottom"><span class="seed">{t2["Seed"]}</span>{person_name(t2)}</li>')
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
        html.append(f'<li class="game game-top">{person_name(t1)} <span class="seed">{t1["Seed"]}</span></li>')
        html.append('<li class="game game-spacer"></li>')
        html.append(f'<li class="game game-bottom">{person_name(t2)} <span class="seed">{t2["Seed"]}</span></li>')
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
