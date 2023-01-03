import re
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# Obteenemos la key de la api.
with open('config.txt', 'r') as f:
    key = str(f.readline().strip())


def extract(equipo):
    link_scrapping = 'https://www.wincomparator.com/es-es/cuotas/baloncesto/usa/nba-id306/'
    season = datetime.now().year
    equipos = requests.get(
        f'https://api.sportsdata.io/v3/nba/scores/json/Allteams?key={key}').json()
    error = True
    team = ''
    for i in equipos:
        if re.search(equipo, i['Name'], re.IGNORECASE):
            team = i['Key']
            error = False
    if error:
        print('El equipo introducido no existe.')
        sys.exit(1)
    players = requests.get(
        f'https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStatsByTeam/{season}/{team}?key={key}').json()
    stats = requests.get(
        f'https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/{season}?key={key}').json()
    for i in range(len(stats)):
        if stats[i]['Team'] == team:
            stats = stats[i]
            break
    page = requests.get(link_scrapping)
    soup = BeautifulSoup(page.content, 'html.parser')
    return players, stats, soup


def transform(equipo, players, stats, soup):
    cuotas = []
    importantes = ['Name', 'Minutes', 'FieldGoalsMade', 'FieldGoalsAttempted', 'TwoPointersMade', 'TwoPointersAttempted',
                   'ThreePointersMade', 'ThreePointersAttempted', 'FreeThrowsMade', 'FreeThrowsAttempted', 'OffensiveRebounds',
                   'DefensiveRebounds', 'Assists', 'Steals', 'BlockedShots', 'Turnovers', 'PersonalFouls', 'Points',
                   'TrueShootingAttempts', 'TrueShootingPercentage',
                   'FantasyPoints', 'PlayerEfficiencyRating']
    local = [i.text for i in soup.find_all('span', class_='mr-2')]
    visitante = [i.text for i in soup.find_all('span', class_='ml-2')]
    idx = -1
    # Parte web scrapping.
    for i in range(len(local)):
        if re.search(equipo, local[i], re.IGNORECASE) or re.search(equipo, visitante[i], re.IGNORECASE):
            idx = i
    if idx == -1:  # No encuentra el partido
        print('No se espera un partido en los proximos dias del equipo escogido.')
    else:  # Si lo encuentra sacamos las cuotas.
        div_importante = soup.find('div', id='list-wrapper')
        partidos = list(div_importante.children)
        for i in range(5, 5+2*(len(visitante)), 2):  # Se encuentran cada dos.
            aux = list(partidos[i].children)[1].find_all('span')
            cuotas.append((float(aux[3].text.strip()),
                          float(aux[6].text.strip())))
        if cuotas[idx][0] > cuotas[idx][1]:
            # Suponiendo que la casa de apuestas se queda con un margen del 3 por ciento.
            print(
                f'Se espera que el equipo {visitante[idx]} gane a {local[idx]} con una probabilidad del {97/cuotas[idx][1]} % ')
        else:
            print(
                f'Se espera que el equipo {local[idx]} gane a {visitante[idx]} con una probabilidad del {97/cuotas[idx][0]} %')
    # Ahora hora del pdf.
    limpio = []
    for i in players:
        aux = {}
        for j in importantes:
            aux[j] = i[j]
        limpio.append(aux)
    df = pd.DataFrame.from_dict(limpio)
    return df


def load(df):
    # En formato html queda mas bonito porque permite deslizar la tabla. Se da de las dos formas.
    df.to_html('out/tabla.html')
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                         colLabels=df.columns, loc='center')
    pp = PdfPages('out/tabla.pdf')
    pp.savefig(fig, bbox_inches='tight')
    pp.close()


if __name__ == '__main__':
    equipo = input(
        'Introduce el nombre del equipo del que deseas obtener informacion: ').split()[-1].strip()
    players, stats, soup = extract(equipo)
    df = transform(equipo, players, stats, soup)
    load(df)
