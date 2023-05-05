import pymongo
import time
import logging

from scrapers.region_scraper import get_all_regions
from scrapers.platform_scraper import get_all_platforms
from scrapers.game_scraper import get_all_games
from scrapers.series_scraper import get_all_series

### --- Variables --- ###
logging.basicConfig(filename='main.log', level=logging.INFO, filemode='w')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["cbd_speedrun_scraper"]

### --- Utils --- ###


### --- Functions --- ###


### --- Executions --- ###

# Regions
regions_start_time = time.time()

logging.info("Starting region scraping...")
region_col = mydb["regions"]
region_col.drop()
get_all_regions(region_col)

regions_end_time = time.time() - regions_start_time
logging.info(f"Region scraping took {regions_end_time} seconds")
print(f"Region scraping took {regions_end_time} seconds")

# Platforms
platforms_start_time = time.time()

logging.info("Starting platform scraping...")
plat_col = mydb["platforms"]
plat_col.drop()
get_all_platforms(plat_col)

platforms_end_time = time.time() - platforms_start_time
logging.info(f"Platform scraping took {platforms_end_time} seconds")

# Game
games_start_time = time.time()

logging.info("Starting game scraping...")
game_col = mydb["games"]
game_col.drop()

cat_col = mydb["categories"]
cat_col.drop()

level_col = mydb["levels"]
level_col.drop()

var_col = mydb["variables"]
var_col.drop()

get_all_games(game_col, cat_col, level_col, var_col)

games_end_time = time.time() - games_start_time
logging.info(f"Game scraping took {games_end_time} seconds")

# Series
series_start_time = time.time()

logging.info("Starting series scraping...")
ser_col = mydb["series"]
ser_col.drop()
get_all_series(ser_col)

series_end_time = time.time() - series_start_time
logging.info(f"Series scraping took {series_end_time} seconds")