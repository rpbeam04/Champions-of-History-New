import json
from pathlib import Path
import random
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from src.utils import generate_seed_order, generate_full_bracket_html


BASE_DIR = Path(__file__).resolve().parents[1]


def data_path(name):
    p = BASE_DIR / 'data' / name
    if p.exists():
        return p
    return BASE_DIR / name


def template_path(name):
    p = BASE_DIR / 'templates' / name
    if p.exists():
        return p
    return BASE_DIR / name


@st.cache_data
def load_participants():
    with open(data_path('participants.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


@st.cache_data
def load_regions():
    return pd.read_csv(data_path('regions.csv'))


def build_people_list(participants):
    # assign seeds if not present
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
    return people


def write_output_html(html_str, name='bracket_preview.html'):
    out_dir = BASE_DIR / 'outputs'
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / name
    out_path.write_text(html_str, encoding='utf-8')
    return out_path


# PDF generation removed — Streamlit will handle previewing. If you need PDF output,
# generate it with the `scripts/generate_bracket.py` script or external tooling.


def main():
    st.title('Champions of History — Bracket Generator')

    participants = load_participants()
    st.sidebar.header('Options')
    preview_button = st.sidebar.button('Preview bracket HTML')

    st.sidebar.markdown('Preview uses the first generated region and a randomized seed placement.')

    if preview_button:
        people = build_people_list(participants)
        regions_df = load_regions()
        regions = []
        for _, row in regions_df.iterrows():
            if row['Region'] != 'Final 32':
                region = {}
                region['Name'] = row['Region'].strip()
                sites = row['First Weekend Sites'].split(';')
                sites = [site.strip() for site in sites]
                region['Sites'] = sites + sites
                region['Final'] = row['Second Weekend Site'].strip()
                regions.append(region)

        html = generate_full_bracket_html(people, regions)
        # Wrap in top template if available
        try:
            top = template_path('BracketTop.html').read_text(encoding='utf-8')
            bottom = '</main></div></body></html>'
            full_html = top + html + bottom
        except Exception:
            full_html = html

        out_html = write_output_html(full_html, name='bracket_preview.html')
        st.success(f'Wrote preview HTML to `{out_html}`')
        # The template now includes a built-in scale wrapper; embed the HTML directly.
        st.html(full_html)

if __name__ == '__main__':
    main()
