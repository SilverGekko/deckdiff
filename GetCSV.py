import re
import time
import string
#import urllib
import requests
import urllib.request
from bs4 import BeautifulSoup

def diff(l1, l2):
    list_diff = l2.copy()
    for item in l1:
        if item in list_diff:
            list_diff.remove(item)
    return list_diff

def deck_swap(lhs, rhs, prices):
    for first, second, price in zip(lhs, rhs, prices):
        print(first, "->", second, "[", price, "]")

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
    # this works but let's throttle requests to the api
    # prices = [requests.get("https://api.scryfall.com/cards/named?exact=" + card_name).json()["prices"]["usd"] for card_name in rhs]
    prices = []
    for card_name in rhs:
        price = requests.get("https://api.scryfall.com/cards/named?exact=" + card_name).json()["prices"]["usd"]
        if price:
            prices.append(float(price))
        else:
            prices.append(0.0)
        time.sleep(.1)
    deck_swap(lhs, rhs, prices)
    print("Total price:", sum(prices))