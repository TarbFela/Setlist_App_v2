import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

song_set = set()




# REAL BOOK LISTEN
BASE_URL = "http://www.realbooklisten.com/index.php"
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a', href=True)
for link in links[4:-2]:
    name = link.contents[0]
    song_set.add(name)





with open("harvest_realbooklisten.txt","w") as f:
    for song in song_set:
        f.write(song + "\n")




