from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import sys
import random
import os
from os import path

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
def getMetacritic():
    req = requests.get('https://www.metacritic.com/game', headers = headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    nums = []
    titles = []
    scores = []
    dates = []
    summaries = []
    clamp = soup.find(class_='clamp-list')
    count = 0

    for i in soup.find_all(class_='title numbered'):
        nums.append(i.get_text().strip())
    for i in clamp.find_all('h3'):
        titles.append(i.get_text().strip())
    for score in clamp.find_all(class_='metascore_w large game positive'):
        if count % 2 == 0:
                scores.append(score.get_text().strip())
        count = count + 1
    count = 0
    for span in soup.find_all(class_='clamp-details'):
        if count % 2 == 1:
            dates.append(span.get_text().strip())
        count = count + 1
    for sum in soup.find_all(class_='summary'):
        summaries.append(sum.get_text().strip())

    data = pd.DataFrame({'Place':nums, 'Title':titles, 'Score':scores, 'Date':dates, 'Summary':summaries})
    data.to_csv('g.csv')

def getTopAiringAnime():
    req = requests.get('https://myanimelist.net/topanime.php?type=airing', headers = headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    ranks = []
    names = []
    scores = []

    for anime in soup.find_all(class_='ranking-list'):
        ranks.append(anime.find(class_='rank ac').get_text().strip())
        n = anime.find(class_='title al va-t word-break').get_text().strip()
        n = re.sub('Watch Promotional Video*', '', n)
        n = re.sub('Watch Episode Video*', '', n)
        n = re.sub('\n.*', '', n)
        names.append(n)
        scores.append(anime.find(class_='score ac fs14').get_text().strip())

    data = pd.DataFrame({'Rank': ranks, 'Name' : names, 'Score':scores})
    if data.empty:
        getTopAiringAnime()
    data.to_csv('Top50AiringAnime.csv')

def getTopAnimeEver():
    req = requests.get('https://myanimelist.net/topanime.php', headers = headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    ranks = []
    names = []
    scores = []

    for anime in soup.find_all(class_='ranking-list'):
        ranks.append(anime.find(class_='rank ac').get_text().strip())
        n = anime.find(class_='title al va-t word-break').get_text().strip()
        n = re.sub('Watch Promotional Video*', '', n)
        n = re.sub('Watch Episode Video*', '', n)
        n = re.sub('\n.*', '', n)
        names.append(n)
        scores.append(anime.find(class_='score ac fs14').get_text().strip())

    data = pd.DataFrame({'Rank': ranks, 'Name' : names, 'Score':scores})
    if data.empty:
        getTopAiringAnime()
    data.to_csv('Top50AnimeEver.csv')

def getTop50Steam():
    req = requests.get('https://store.steampowered.com/search/?filter=topsellers&os=win', headers = headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    v = soup.find(id='search_resultsRows')

    names = []
    ranks = []
    prices = []
    count = 1

    for ent in v.find_all('a'):
        names.append(ent.find(class_='title').get_text().strip())
        ranks.append(count)
        #print(ent.find('br'))
        s = ent.find(class_='col search_price discounted responsive_secondrow')
        if s is not None:
            str = s.get_text().strip()
            str = re.sub('^\$[0-9]*.[0-9]*', '', str)
            prices.append(str)
        else:
            prices.append(ent.find(class_='col search_price_discount_combined responsive_secondrow').get_text().strip())
        count = count + 1

    data = pd.DataFrame({'Rank':ranks, 'Name':names, 'Price':prices})
    data.to_csv('Top50Steam.csv')

def compareTop10Metacritic():
    if path.exists("cMetacritic.csv"):
        df = pd.read_csv("cMetacritic.csv")
        oldf = pd.read_csv("games.csv")
        s = set()
        count = 0
        for row in oldf.iterrows():
            s.add(row[1][2])
        for row in df.iterrows():
            if row[1][1] in s:
                df.DaysatTop[count] = df.DaysatTop[count] + 1
            else:
                df = df.drop(df.index[df.Game == row[1][1]])
            count = count + 1
        print(df)
        df.to_csv('cMetacritic.csv')
    else:
        data = pd.read_csv('games.csv')
        columns = ['Game', 'DaysatTop']
        newdf = pd.DataFrame(columns = columns)
        games = data['title']
        ones = []
        for g in games:
            ones.append(1)
        newdf = pd.DataFrame({'Game':games, 'DaysatTop':ones})
        newdf.to_csv('cMetacritic.csv')

arg_list = sys.argv
compareTop10Metacritic()
x = 0
usage = """                 Usage
           Get Top Airing Anime               -taa
           Get Top Anime Ever                 -tae
           Get Top Metacritic                  -gm
           Get Top Selling Steam               -ts
           Usage                            -usage"""
for arg in arg_list:
    if x == 0:
        x = 1
        continue
    if arg == '-taa':
        getTopAiringAnime()
    elif arg == '-tae':
        getTopAnimeEver()
    elif arg == '-gm':
        getMetacritic()
    elif arg == '-ts':
        getTop50Steam()
    elif arg == '-usage':
        print(usage)
    else:
        print(usage)
