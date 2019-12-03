import re
import string
import urllib
from bs4 import BeautifulSoup

def diff(l1, l2):
    list_diff = l2.copy()
    for item in l1:
        if item in list_diff:
            list_diff.remove(item)
    return list_diff

def deck_swap(lhs, rhs):
    for first, second in zip(lhs, rhs):
        print(first, "->", second)

if __name__ == "__main__":
    deck_lists = []
    urls = [
    "https://tappedout.net/mtg-decks/21-11-19-marchesa-aristocrats/",
    "https://tappedout.net/mtg-decks/varina-kitchen-sink/"]
    for url in urls:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, features="lxml")

        for script in soup(["scriptdeck_lists", "style"]):
            script.extract()

        deck_text = soup.find_all('textarea')
        for area in deck_text:
            if area["id"] == "mtga-textarea":
                deck_text = area
                break

        text = deck_text.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        deck_list = [chunk.rstrip(string.digits + ' ') for chunk in chunks if chunk]
        singleton_list = []
        for card in deck_list:
            qty = card.split(' ')[0]
            name = re.search(r'[A-Za-z]+[A-Za-z \',\-]*(?= \()', card).group(0)
            for x in range(int(qty)):
                singleton_list.append(name)

        deck_lists.append(singleton_list)

    lhs = diff(deck_lists[0], deck_lists[1])
    rhs = diff(deck_lists[1], deck_lists[0])
    deck_swap(lhs, rhs)