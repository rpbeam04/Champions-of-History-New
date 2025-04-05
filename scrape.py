import requests
from bs4 import BeautifulSoup
import re
import json
import wikipediaapi

counts = {3: 0, 4: 0, 5: 0, 6: 0}
cur = {3: None, 4: None, 5: None, 6: None}

def process_people(tag):
    people = []

    level_stack = []  # Keeps track of active heading levels

    ct = 0
    while tag:
        if tag.name and tag.name.startswith('h') and tag.name[1:].isdigit():
            tag_level = int(tag.name[1])
            if tag_level in counts:
                # Adjust level stack
                while level_stack and level_stack[-1] >= tag_level:
                    l = level_stack.pop()
                    cur[l] = None
                level_stack.append(tag_level)

                indent = len(level_stack) - 1
                cur[tag_level] = tag.text

                # Find next paragraph (sibling or nearby)
                p = tag.find_next('p')
                if p:
                    match = re.search(r'\d+', p.text)
                    if match:
                        counts[tag_level] += int(match.group())

        elif tag.name == "ol":
            indent = len(level_stack)
            for li in tag.find_all('li', recursive=False):
                name = li.text.strip().split("(Level 3")
                try:
                    link = li.find('b').find('a', recursive=False)['href']
                except:
                    link = li.find('a', recursive=False)['href']
                person = {"Name": name[0].strip(), "Link": "https://en.wikipedia.org" + link, 
                          "Level 3": True if len(name) > 1 else False,
                          "h3": cur[3], "h4": cur[4], "h5": cur[5], "h6": cur[6]}
                people.append(person)
                ct += 1

        tag = tag.find_next()
    
    return people

def scrape_vital_people():
    # URL = "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/4/People"
    # response = requests.get(URL)
    # soup = BeautifulSoup(response.text, 'html.parser')

    with open("WikiArticle.html","r",encoding="utf-8") as f:
        response = f.read()
        soup = BeautifulSoup(response, 'html.parser')

    content_div = soup.find("div", class_="mw-content-ltr mw-parser-output")

    people = process_people(content_div.find_next('h3'))

    with open("vital_people.json", "w", encoding="utf-8") as f:
        json.dump(people, f, indent=2)

    return people

def article_length(name, wiki_wiki):
    page = wiki_wiki.page(name)
    return len(page.text), page.summary.split('\n')[0]
