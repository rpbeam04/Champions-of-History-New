import requests
from bs4 import BeautifulSoup
from pprint import *
import os
import pandas as pd
import json

url = "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/4/People"
filename = "WikiArticle.html"

# Check if the file has been saved already today
if os.path.exists(filename) and os.path.getmtime(filename) > pd.Timestamp.today().floor("D").timestamp():
  print("I have a file!")
  with open(filename, "r") as f:
    html = f.read()
else:
  # Scrape the URL and save the HTML file
  response = requests.get(url)
  print("I'm scraping!")
  html = response.text
  with open(filename, "w") as f:
    f.write(html)

soup = BeautifulSoup(html, "html.parser")
links = soup.find_all("a")

articles = []
rogues = ["Articles related to current events","The hub for editors"]
with open("Invitees.txt") as f:
  invitees = f.read().split("\n")
  for i,invite in enumerate(invitees):
    article_url = "https://en.wikipedia.org/wiki/" + invite.replace(" ", "_")
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, "html.parser")
    word_count = len(article_soup.get_text().split())
    invitees[i] = ({"Name": invite, "URL": article_url, "WordCount": word_count})

for link in links:
  name = link.get("title")
  try:
    split_url = link.get("href").split("/")
  except:
    split_url = []
  if name and len(split_url) == 3 and split_url[1] == "wiki" and " article" not in name and ":" not in name and "[" not in name and "Wikipedia" not in name and name not in rogues:
    article_url = "https://en.wikipedia.org/wiki/" + name.replace(" ", "_")
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, "html.parser")
    word_count = len(article_soup.get_text().split())
    articles.append({"Name": name, "URL": article_url, "WordCount": word_count})

articles = articles + invitees
pprint(len(articles))
pprint(invitees)
articles = sorted(articles, key = lambda x: x['Name'])

with open("People.txt",'w') as f:
  for article in articles:
    f.write(f"{article['Name']}\n")

with open("People_Dicts.json",'w') as f:
  json.dump(articles, f, indent = 2)