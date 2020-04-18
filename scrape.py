from bs4 import BeautifulSoup
import pandas as pd
import requests

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
req = requests.get('https://www.metacritic.com/game', headers = headers)
soup = BeautifulSoup(req.content, 'html.parser')

gametable = soup.find(class_='clamp-list')
print(gametable)
