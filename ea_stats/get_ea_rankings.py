

##############
# Author: Jordan Runco
# 
# This code downloads player ratings from EA's website and organizes them by team
##############


import numpy as np 
import pandas as pd
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os



#url = "https://www.ea.com/games/nhl/ratings" # page 1
#url = "https://www.ea.com/games/nhl/ratings?page=2" # page 2
url = "https://www.ea.com/games/nhl/ratings/player-ratings/connor-mc-david/9857" # single player

### these two blocks of text do the same thing
response = requests.get(url)
print(f"Status Code: {response.status_code}")
#print(response.text)

page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")


dfs = pd.read_html(response.text)




















"""
try:
    response = requests.get(url)
    response.raise_for_Status()

    test = 

except requests.exceptions.RequestException as e:
    print(f"Error making the request: {e}")
except ValueError:
    print("Error parsing JSON response. Check if the URL returns valid JSON.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
"""