import json
from pprint import *
from bracket import bracket
import math
import random
from collections import Counter

with open("People_Dicts.json","r") as f:
  data = json.load(f)

for i,d in enumerate(data):
  data[i]["Rating"] = round(d["WordCount"]/1000 + 50)

def get_rating(name):
  for d in data:
    if d['Name'] == name:
      return d['Rating']
  return None
def get_true_seed(name):
  return tourney.teams.index(name)+1
def get_seed(name):
  return math.ceil((tourney.teams.index(name)+1)/32)

data = sorted(data, key = lambda x: x['WordCount'], reverse = True)

tourney = bracket.Bracket([i["Name"] for i in data])

with open("Rankings.txt",'w') as f:
  for team in tourney.teams:
    f.write(f"{get_seed(team)}. {team}\n")  

with open("FirstRound.txt","w") as f:
  c = 1
  for seed in tourney.lineup:
    if (c-1)%64 == 0:
      f.write(f"--REGION {int((c-1)/64 +1)}--\n")
    f.write(f"{math.ceil(seed/32)}. {tourney.teams[seed-1]} ({get_rating(tourney.teams[seed-1])})\n")
    if c%2==0:
      f.write("\n")
    c+=1

def win_probability():
  return None

def matchup(team1,team2):
  w1 = 1/(1+math.e**(-0.18*(get_rating(team1)-75)))
  w2 = 1/(1+math.e**(-0.18*(get_rating(team2)-75)))
  return random.choices([team1,team2],weights=[w1,w2])[0]

champions = []
for u in range(0,1):
  matchups = [x for x in tourney.lineup]
  for r in range(1,len(tourney.rounds)):
    next_round = []
    winners = []
    for c,seed in enumerate(matchups):
      if c%2==0:
        winner = matchup(tourney.teams[matchups[c+1]-1],tourney.teams[matchups[c]-1])
        winners.append(winner)
        next_round.append(get_true_seed(winner))
    tourney.update(r+1,winners)
    matchups = next_round
  champions.append(tourney.rounds[-1][0])
  if u%10==0:
    print(f"{u}:\n")
    last_8 = tourney.rounds[-4:]
    pprint(last_8)
    for i,round in enumerate(last_8):
      last_8[i] = [get_seed(x) for x in round]
    pprint(last_8)
    print("\n\n")
  tourney = bracket.Bracket([i["Name"] for i in data])

counted = dict(Counter(champions))
champs_dicts = []
for key, val in counted.items():
  champs_dicts.append({"name":key,"seed":get_seed(key),"wins":val})
del(counted)
champs_dicts = sorted(champs_dicts, key = lambda x: x["seed"])
pprint(champs_dicts)
print("\n___________\n")

# for i,d in enumerate(results):
#   results[i]["seed"] = get_seed(d['name'])

# seed_cts = []
# for i in range(1,17):
#   seed_cts.append({"seed":i,"wins":0})
# for d in results:
#   seed_cts[d["seed"]-1]["wins"]+=d["wins"]
# for i,d in enumerate(seed_cts):
#   seed_cts[i]["pct"] = d["wins"]/10
# pprint(seed_cts)

def generate_bracket_html(teams):
    # Determine the number of rounds needed for the bracket
    num_rounds = math.ceil(math.log2(len(teams)))

    # Initialize the bracket HTML
    bracket_html = '<div class="tournament-bracket">'

    # Generate the HTML for each round of the bracket
    for round_num in range(num_rounds):
        round_html = '<div class="bracket-round">'
        for match_num in range(2 ** (num_rounds - round_num - 1)):
            team1_index = match_num * 2
            team2_index = match_num * 2 + 1
            team1 = teams[team1_index] if team1_index < len(teams) else ''
            team2 = teams[team2_index] if team2_index < len(teams) else ''
            match_html = f'<div class="bracket-match"><span class="team">{team1}</span><span class="team">{team2}</span></div>'
            round_html += match_html
        round_html += '</div>'
        bracket_html += round_html

    # Close the bracket HTML
    bracket_html += '</div>'

    return bracket_html

def generate_first_round_html(teams):
    # Determine the number of rounds needed for the bracket
    num_rounds = math.ceil(math.log2(len(teams)))

    # Initialize the bracket HTML
    bracket_html = '<div class="tournament-bracket">'

    # Generate the HTML for the first round of the bracket
    round_num = 0
    round_html = '<div class="bracket-round">'
    for match_num in range(2 ** (num_rounds - round_num - 1)):
        team1_index = match_num * 2
        team2_index = match_num * 2 + 1
        team1 = teams[team1_index] if team1_index < len(teams) else ''
        team2 = teams[team2_index] if team2_index < len(teams) else ''
        match_html = f'<div class="bracket-match"><span class="team">{team1}</span><span class="team">{team2}</span></div>'
        round_html += match_html
    round_html += '</div>'
    bracket_html += round_html

    # Close the bracket HTML
    bracket_html += '</div>'

    return bracket_html


html = generate_first_round_html([tourney.teams[x-1] for x in tourney.lineup[:64]])

# from bracketeer import build_bracket

# seeds = []
# for i,seed in enumerate(tourney.lineup):
#   if i%2==1:
#     true_pair = []
#     pair = [math.ceil(seed/32),math.ceil(tourney.lineup[i-1]/32)]
#     pair.sort()
#     seeds.append(pair)
# b = build_bracket(teamsPath="",seedsPath="")

# html = b.render()

with open("Bracket.html","w") as f:
  f.write(html)