from time import sleep
import requests
import urllib3
from bs4 import BeautifulSoup

# This is also me learning how to web-scrape properly
# Functions taken from https://github.com/LearnDataSci/article-resources/blob/master/Ultimate%20Guide%20to%20Web%20Scraping/Part%201%20-%20Requests%20and%20BeautifulSoup/notebook.ipynb

#############################Functions#########################################


def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()


############################Initial Page Scrape#################################
url_advanced = r'https://www.basketball-reference.com/leagues/NBA_2010_advanced.html'
r = requests.get(url_advanced)
print(r.content[:100])  # this is to check if we actually have the url

soup = BeautifulSoup(r.content, 'html.parser')
rows = soup.select('tbody tr')

row = rows[0]
print(row)
name = row.select_one('[data-stat=player]').text.strip()
print(name)

team = row.select_one('[data-stat=team_id]').text.strip()
print(team)

gp = int(row.select_one('[data-stat=g]').text.strip())
print(f"Arron Afflalo played {gp} games during the 2009-10 NBA season")

#####################Multiple Advanced Page Scrape###########################
# Advanced stats from 2010-2018
advanced_pages = [
    r'https://www.basketball-reference.com/leagues/NBA_2010_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2011_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2012_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2013_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2014_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2015_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2016_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2017_advanced.html',
    r'https://www.basketball-reference.com/leagues/NBA_2018_advanced.html'
]

data = []
year = 2010  # This can be changed to whatever the starting year is

for page in advanced_pages:
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('tbody tr')

    for row in rows:
        d = dict()
        # The initial scraping threw back some errors, this is to address those specific erros
        if row.select_one('[data-stat=g]').text.strip() != 'G' and row.select_one('[data-stat=per]').text.strip() != "" and row.select_one('[data-stat=ts_pct]').text.strip() != "":
            d['Year'] = year
            d['Name'] = row.select_one('[data-stat=player]').text.strip()
            d['Position'] = row.select_one('[data-stat=pos]').text.strip()
            d['Team'] = row.select_one('[data-stat=team_id]').text.strip()
            d['Games_Played'] = float(
                row.select_one('[data-stat=g]').text.strip())
            d['Minutes_Played'] = float(
                row.select_one('[data-stat=mp]').text.strip())
            d['PER'] = float(row.select_one('[data-stat=per]').text.strip())
            d['TS_Percentage'] = float(row.select_one(
                '[data-stat=ts_pct]').text.strip())
            d['3PAr'] = float(row.select_one(
                '[data-stat=fg3a_per_fga_pct]').text.strip())
            d['FTr'] = float(row.select_one(
                '[data-stat=fta_per_fga_pct]').text.strip())
            d['ORB_Percentage'] = float(row.select_one(
                '[data-stat=orb_pct]').text.strip())
            d['DRB_Percentage'] = float(row.select_one(
                '[data-stat=drb_pct]').text.strip())
            d['TRB_Percentage'] = float(row.select_one(
                '[data-stat=trb_pct]').text.strip())
            d['AST_Percentage'] = float(row.select_one(
                '[data-stat=ast_pct]').text.strip())
            d['STL_Percentage'] = float(row.select_one(
                '[data-stat=stl_pct]').text.strip())
            d['BLK_Percentage'] = float(row.select_one(
                '[data-stat=blk_pct]').text.strip())
            d['TOV_Percentage'] = float(row.select_one(
                '[data-stat=tov_pct]').text.strip())
            d['USG_Percentage'] = float(row.select_one(
                '[data-stat=usg_pct]').text.strip())
            d['OWS'] = float(row.select_one('[data-stat=ows]').text.strip())
            d['DWS'] = float(row.select_one('[data-stat=dws]').text.strip())
            d['WS'] = float(row.select_one('[data-stat=ws]').text.strip())
            d['OBPM'] = float(row.select_one('[data-stat=obpm]').text.strip())
            d['DBPM'] = float(row.select_one('[data-stat=dbpm]').text.strip())
            d['BPM'] = float(row.select_one('[data-stat=bpm]').text.strip())
            d['VORP'] = float(row.select_one('[data-stat=vorp]').text.strip())

            data.append(d)

    year += 1
    sleep(5)

print(data[0])
