from bs4 import BeautifulSoup
import pandas as pd
import requests
from tkinter import  *

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
        names.append(anime.find(class_='title al va-t word-break').get_text().strip())
        scores.append(anime.find(class_='score ac fs14').get_text().strip())

    data = pd.DataFrame({'Rank': ranks, 'Name' : names, 'Score':scores})
    if data.empty:
        getTopAiringAnime()
    print(data)
    data.to_csv('Top 50 Airing Anime')




getTopAiringAnime()
