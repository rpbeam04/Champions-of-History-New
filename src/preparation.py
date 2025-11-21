from src.scrape import scrape_vital_people, article_length
import pandas as pd
import json
import wikipediaapi
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def data_path(name):
    p = BASE_DIR / 'data' / name
    if p.exists():
        return p
    p = BASE_DIR / name
    return p


# Scrape Wikipedia for Vital People
# people = scrape_vital_people()
with open(data_path('vital_people.json'), 'r', encoding='utf-8') as f:
    people = json.load(f)

# Load invitees into dataset
invitees = pd.read_csv(data_path('invitees.csv'))
invitees['Level 3'] = False
json_str = invitees.to_json(orient='records', indent=2)
invitees = json.loads(json_str)
json_str = json_str.replace('\\/', '/')

with open(data_path('invitees.json'), 'w', encoding='utf-8') as f:
    f.write(json_str)

# Obtain article lengths
people = people + invitees

wiki_wiki = wikipediaapi.Wikipedia(user_agent='HistoryMadness (rpbeam@icloud.com)', language='en')

for i, person in enumerate(people):
    if i < 3000:
        if i % 20 == 0:
            print(i)
        article_len, summary = article_length(person['Name'], wiki_wiki)
        people[i]['Length'] = article_len
        people[i]['Summary'] = summary
    else:
        people[i]['Length'] = 0
        people[i]['Summary'] = ''

# Sort by word count and Level 3
people = sorted(people, key=lambda x: x['Length'], reverse=True)
people = sorted(people, key=lambda x: x['Level 3'], reverse=True)

# Write whole field to json
with open(data_path('participants.json'), 'w', encoding='utf-8') as f:
    json.dump(people, f, indent=2)
