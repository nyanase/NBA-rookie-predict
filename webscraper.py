from bs4 import BeautifulSoup
import urllib.request
import csv
import sys

#specify the url
domain = 'https://www.basketball-reference.com'
urlpage = 'https://www.basketball-reference.com/players/'

page = urllib.request.urlopen(urlpage)

soup = BeautifulSoup(page, 'html.parser')

features = ['Name', 'Season', 'Age', 'Team', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', 
             '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 
             'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'AS']
rows = []
rows.append(features)

def iter_all():
  alphabet = 'abcdefghijklmnopqrstuvwyz'
  
  for i in range(len(alphabet)):
    letter_page = urllib.request.urlopen(urlpage + "%c/" % alphabet[i])
    letter_soup = BeautifulSoup(letter_page, 'html.parser')
  
    get_player_data(letter_soup)
    print("Finished", alphabet[i])


def get_player_data(soup):
  players = soup.find(attrs={'id': 'all_players'}).find('tbody').find_all('tr')
  for player in players:
    gen_stats = player.find_all('td')
    if int(gen_stats[0].getText()) < 1990 or int(gen_stats[1].getText()) - int(gen_stats[0].getText()) < 3:
      continue

    stat_list = []
      
    name = player.find('th').find('a').getText()
    stat_list.append(name)
    
    player_url = player.find('th').find('a').get('href')
    player_page = urllib.request.urlopen(domain + player_url)
    player_soup = BeautifulSoup(player_page, 'html.parser')
    
    rookie_szn_stats = player_soup.find(attrs={'id': 'per_game'}).find('tbody').find('tr')
    
    if rookie_szn_stats.find('th'):  
      season = rookie_szn_stats.find('th').find('a').getText()
    else:
      season = ''
    stat_list.append(season)
    
    rookie_ind_stats = rookie_szn_stats.find_all('td')
        
    for i in range(len(rookie_ind_stats)):
      if (rookie_ind_stats[i].find('a')):
        stat_list.append(rookie_ind_stats[i].find('a').getText())
      else:
        stat_list.append(rookie_ind_stats[i].getText())
      
    if player_soup.find(attrs={'id': 'bling'}):
      if player_soup.find(attrs={'id': 'bling'}).find(attrs={'class': 'all_star'}):
        stat_list.append(True)    
      else:
        stat_list.append(False)
    else:
      stat_list.append(False)
    
    print('.', end='')
    sys.stdout.flush()
    rows.append(stat_list)
    
  return 

def to_csv():
  with open('players.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)

iter_all()
to_csv()
