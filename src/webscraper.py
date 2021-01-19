import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error


summon_dict = {}
attack_dict = {}


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
        except IndexError:
            print(name)


def get_quotes_from_expansion(expansion_name):
    url = 'https://hearthstone.gamepedia.com/' + expansion_name
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
    print(expansion_name + " finished")


def create_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('CREATE TABLE Quotes (Name, Summon, Attack)')
        for key in summon_dict:
            c.execute('INSERT INTO Quotes VALUES (?, ?, ?)',
                      (key, summon_dict[key], 'None'))
        for key in attack_dict:
            attack_quote = attack_dict[key]
            c.execute('SELECT 1 FROM Quotes WHERE Name = ?', (key,))
            exist = c.fetchone()
            if exist is None:
                c.execute('INSERT INTO Quotes VALUES (?, ?, ?)',
                          (key, 'None', attack_quote))
            else:
                c.execute('UPDATE Quotes SET Attack = ? WHERE Name = ?',
                          (attack_quote, key))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


path = r"C:\Users\seanh\Desktop\Projects\HearthstoneWebScraper\Hearthstone-Quote-Web-Scraper\quotes.db"

# A list of all the expansion names that are currently available
expansions = ['Basic', 'Classic', 'Rise_of_Shadows', 'Saviors_of_Uldum', 'Descent_of_Dragons', 'Galakrond\'s_Awakening',
              'Demon_Hunter_Initiate', 'Ashes_of_Outland', 'Scholomance_Academy', 'Madness_at_the_Darkmoon_Faire', 'Hall_of_Fame',
              'Curse_of_Naxxramas', 'Goblins_vs_Gnomes', 'Blackrock_Mountain', 'The_Grand_Tournament', 'The_League_of_Explorers',
              'Whispers_of_the_Old_Gods', 'One_Night_in_Karazhan', 'Mean_Streets_of_Gadgetzan', 'Journey_to_Un\'Goro',
              'Knights_of_the_Frozen_Throne', 'Kobolds_%26_Catacombs', 'The_Witchwood', 'The_Boomsday_Project', 'Rastakhan\'s_Rumble']

for name in expansions:
    get_quotes_from_expansion(name)

# get_quotes_from_expansion(expansions[3])

create_db(path)

# print(summon_dict)
# print(attack_dict)
print("Done")
