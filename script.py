import requests
from bs4 import BeautifulSoup
import datetime

r = requests.get('http://www.tabeladobrasileirao.net/')

soup = BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
table_html = soup.find('tbody')

fla_home = []
fla_away = []

for row in table_html.findAll("tr"):
    game = dict()
    match = row["data-round"]
    game['round'] = int(match)

    date_string = row.find('div', {"class": "game-date"}).find(text=True)
    date = '{}'.format(date_string.split()[2])
    hour = '{}'.format(date_string.split()[4])
    game_date = str(date + " " + hour)
    #data_formatada = datetime.datetime.strptime(game_date, "%d/%m/%Y %H:%M")
    game['date'] = datetime.datetime.strptime(game_date, "%d/%m/%Y %H:%M")

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

    if(game['home_team'] == "Flamengo"):
        fla_home.append(game)
    if(game['away_team'] == "Flamengo"):
        fla_away.append(game)
print("JOGOS EM CASA DO MENGÃO:")
for casa in fla_home:
    print("Dia: {} | {} x {}".format(casa['date'].strftime("%d/%m/%Y as %H:%M"),casa['home_team'], casa['away_team']))
print("JOGOS FORA DE CASA DO MENGÃO:")
for fora in fla_away:
    print("Dia: {} | {} x {}".format(fora['date'].strftime("%d/%m/%Y as %H:%M"),fora['home_team'], fora['away_team']))
