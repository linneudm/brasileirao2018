import requests
from bs4 import BeautifulSoup
import time
import datetime

r = requests.get('http://www.tabeladobrasileirao.net/')

soup = BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
table_html = soup.find('tbody')

for row in table_html.findAll("tr"):
    game = dict()
    match = row["data-round"]
    game['round'] = int(match)

    date_string = row.find('div', {"class": "game-date"}).find(text=True)
    #date_string = '{}/{}'.format(date_string.split(), date_string.split())
    date_string = date_string.split()[2]
    #print(date_string)
    game['date'] = datetime.datetime.strptime(date_string, "%d/%m/%Y").date()

    game['home_team'] = row.find('div', {"class": "game-club--principal"})['title']
    result = row.findAll('div', {"class": "game-scoreboard-input"})
    home_team_result = result[0].find(text=True)
    away_team_result = result[2].find(text=True)

    try:
        game['home_team_result'] = int(home_team_result)
        game['away_team_result'] = int(away_team_result)
    except ValueError:
        game['home_team_result'] = None
        game['away_team_result'] = None

    game['away_team'] = row.find('div', {"class": "game-club--visitor"})['title']

    #if(game['home_team'] == "Flamengo" or game['away_team'] == "Flamengo"):
    #    print(game)
    print(game)
