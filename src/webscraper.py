import requests
from bs4 import BeautifulSoup


summon_dict = {}
attack_dict = {}
death_dict = {}


# Pass in the href of a card to retrieve its summon and attack quotes
def get_quotes(name, href):
    url = 'https://hearthstone.gamepedia.com' + href
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.find_all('dl')
    for tag in tags:
        try:
            quote_action = tag.find_all('dt')
            # ith quote should always be associated with the ith action.
            for i in range(len(quote_action)):
                if quote_action[i].string == 'Summon':
                    summon_dict[name] = tag.find_all('dd')[i].find('i').string
                elif quote_action[i].string == 'Attack':
                    attack_dict[name] = tag.find_all('dd')[i].find('i').string
        except AttributeError:
            continue


dict = {}
url = 'https://hearthstone.gamepedia.com/The_Boomsday_Project'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# Finds all <a> tags
tags = soup.find_all('a')
# Iterates through all the tags, looking for those with an associated <img>, <href>, and <title> tags
for tag in tags:
    title = tag.get('title')
    href = tag.get('href')
    img = tag.find('img')
    if img == None:
        continue
    # The dimensions of the images of the cards
    if img.get('width') == '200' and img.get('height') == '276':
        get_quotes(title, href)
print(summon_dict)
print(attack_dict)
