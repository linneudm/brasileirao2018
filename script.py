import requests
from bs4 import BeautifulSoup
import datetime
import sys
from unicodedata import normalize


def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

class BuscarJogosBrasileirao():
    def __init__(self, time, site):
        self.site = site
        self.time = time

    def get_jogos(self):
        time = self.time
        time = remover_acentos(time)
        r = requests.get(self.site)

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

            if(remover_acentos(game['home_team'].lower()) == time.lower()):
                fla_home.append(game)
            if(remover_acentos(game['away_team'].lower()) == time.lower()):
                fla_away.append(game)
        if(len(fla_home) > 0):
            print("JOGOS EM CASA DO {time}:".format(time=time))
            for casa in fla_home:
                print("Dia: {} | {} x {}".format(casa['date'].strftime("%d/%m/%Y as %H:%M"),casa['home_team'], casa['away_team']))
        else:
            print('Não foi possível encontrar os jogos dentro de casa para {time}.'.format(time=time))
        if(len(fla_away) > 0):
            print("JOGOS FORA DE CASA DO {time}:".format(time=time))
            for fora in fla_away:
                print("Dia: {} | {} x {}".format(fora['date'].strftime("%d/%m/%Y as %H:%M"),fora['home_team'], fora['away_team']))
        else:
            print('Não foi possível encontrar os jogos fora de casa para {time}.'.format(time=time))


time = sys.argv[1]
if(len(sys.argv) > 2):
    site = sys.argv[2]
else:
    site = 'http://www.tabeladobrasileirao.net/'

brasileirao = BuscarJogosBrasileirao(time, site)
brasileirao.get_jogos()