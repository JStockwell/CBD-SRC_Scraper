import logging

from utils.scrapers import scrape_regions, scrape_platforms, scrape_games, scrape_series

### --- Variables --- ###
logging.basicConfig(filename='main.log', level=logging.INFO, filemode='w')

MAX_GAME_CALLS = 10

### --- Utils --- ###


### --- Functions --- ###


### --- Executions --- ###
# regions, platforms, series, games
flags = [False] * 4

flags[0] = input("Scrape regions? (y/n) ") == "y"
flags[1] = input("Scrape platforms? (y/n) ") == "y"
flags[2] = input("Scrape series? (y/n) ") == "y"
flags[3] = input("Scrape games? (y/n) ") == "y"

if flags[0]:
    scrape_regions()

if flags[1]:
    scrape_platforms()

if flags[2]:
    scrape_series()

if flags[3]:
    offset = int(input("Offset: "))
    MAX_GAME_CALLS = int(input("Max game calls: "))
    clear_db = input("Clear database? (y/n) ") == "y"
    scrape_games(offset, MAX_GAME_CALLS, clear_db)