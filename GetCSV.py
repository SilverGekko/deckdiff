import re
import csv
import string
import urllib
from bs4 import BeautifulSoup

url = "https://tappedout.net/mtg-decks/21-11-19-marchesa-aristocrats/"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, features="lxml")

for script in soup(["script", "style"]):
    script.extract()

# text_areas = soup.find_all('textarea')
deck_text = soup.find_all('textarea')

for area in deck_text:
    if area["id"] == "mtga-textarea":
        deck_text = area
        break

text = deck_text.get_text()

lines = (line.strip() for line in text.splitlines())

chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

# text = '\n'.join(chunk.rstrip(string.digits) for chunk in chunks if chunk)

deck_list = [chunk.rstrip(string.digits + ' ') for chunk in chunks if chunk]

# print(text)
print(deck_list)

board_list = []
qty_list = []
name_list = []
printing_list = []

csv_list = []

for line in deck_list:
    qty = int(line.split(' ')[0])
    # print(line)
    name = re.search(r'[A-Za-z]+[A-Za-z \',]*(?= \()', line)
    printing = re.search(r'(?<=\()[A-Z]+[0-9]*(?=\))', line)
    board_list.append("main")
    qty_list.append(qty)
    # name_list.append(name.group(0)) if name else name_list.append('')
    if name:
        # print(name.group(0))
        name_list.append(name.group(0))
    else:
        # print("name failed")
        name_list.append('')
    printing_list.append(printing.group(0)) if printing else printing_list.append('')

# print(board_list)
# print(qty_list)
# print(name_list)
# print(printing_list)
# print(sum(qty_list))
# print(len(board_list), len(qty_list), len(name_list), len(printing_list))

mapped = zip(board_list, qty_list, name_list, printing_list)
mapped = list(mapped)
# print(mapped)

with open('deck1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Board', "Qty", "Name", "Printing"])
    for line in mapped:
        writer.writerow(line)