import json
import re

import requests
from bs4 import BeautifulSoup

from .paths import data_path

counts = {3: 0, 4: 0, 5: 0, 6: 0}
cur = {3: None, 4: None, 5: None, 6: None}


def process_people(tag):
    people = []
    level_stack = []

    while tag:
        if tag.name and tag.name.startswith("h") and tag.name[1:].isdigit():
            tag_level = int(tag.name[1])
            if tag_level in counts:
                while level_stack and level_stack[-1] >= tag_level:
                    level = level_stack.pop()
                    cur[level] = None
                level_stack.append(tag_level)
                cur[tag_level] = tag.text

                paragraph = tag.find_next("p")
                if paragraph:
                    match = re.search(r"\d+", paragraph.text)
                    if match:
                        counts[tag_level] += int(match.group())
        elif tag.name == "ol":
            for li in tag.find_all("li", recursive=False):
                name = li.text.strip().split("(Level 3")
                try:
                    link = li.find("b").find("a", recursive=False)["href"]
                except AttributeError:
                    link = li.find("a", recursive=False)["href"]
                people.append(
                    {
                        "Name": name[0].strip(),
                        "Link": "https://en.wikipedia.org" + link,
                        "Level 3": len(name) > 1,
                        "h3": cur[3],
                        "h4": cur[4],
                        "h5": cur[5],
                        "h6": cur[6],
                    }
                )

        tag = tag.find_next()

    return people


def scrape_vital_people():
    with open(data_path("WikiArticle.html"), "r", encoding="utf-8") as handle:
        soup = BeautifulSoup(handle.read(), "html.parser")

    content_div = soup.find("div", class_="mw-content-ltr mw-parser-output")
    people = process_people(content_div.find_next("h3"))

    with open(data_path("vital_people.json"), "w", encoding="utf-8") as handle:
        json.dump(people, handle, indent=2)

    return people


def article_length(name, wiki_wiki):
    page = wiki_wiki.page(name)
    return len(page.text), page.summary.split("\n")[0]
