import random
import json
import pandas as pd
from pathlib import Path
from src.utils import generate_seed_order, generate_full_bracket_html

BASE_DIR = Path(__file__).resolve().parents[1]

def data_path(name):
    p = BASE_DIR / 'data' / name
    if p.exists():
        return p
    p = BASE_DIR / name
    return p


def template_path(name):
    p = BASE_DIR / 'templates' / name
    if p.exists():
        return p
    p = BASE_DIR / name
    return p


if __name__ == '__main__':
    with open(data_path('participants.json'), 'r', encoding='utf-8') as f:
        participants = json.load(f)

    seed = 0
    for i, person in enumerate(participants):
        if i % 32 == 0:
            seed += 1
        person['Seed'] = seed

    seeds = generate_seed_order(64)
    people = []
    for s in seeds:
        r = random.randint((s - 1) * 32, s * 32 - 1)
        people.append(participants[r])
        assert participants[r]['Seed'] == s, f"{participants[r]['Seed']} {s}"

    region_data = pd.read_csv(data_path('regions.csv'))
    regions = []
    for _, row in region_data.iterrows():
        if row['Region'] != 'Final 32':
            region = {}
            region['Name'] = row['Region'].strip()
            sites = row['First Weekend Sites'].split(';')
            sites = [site.strip() for site in sites]
            region['Sites'] = sites + sites
            region['Final'] = row['Second Weekend Site'].strip()
            regions.append(region)

    bracket = generate_full_bracket_html(people, regions)

    with open(template_path('BracketTop.html'), 'r', encoding='utf-8') as f:
        bracket_top = f.read()
        bracket_bottom = '</main></div></body></html>'

    html = bracket_top + bracket + bracket_bottom

    out_dir = BASE_DIR / 'outputs'
    out_dir.mkdir(exist_ok=True)
    # import weasyprint only when actually generating the PDF to avoid hard dependency on import time
    from weasyprint import HTML
    HTML(string=html).write_pdf(out_dir / 'output.pdf')
