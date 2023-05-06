import time
import logging
import pymongo

from scrapers.region_scraper import get_all_regions
from scrapers.platform_scraper import get_all_platforms
from scrapers.game_scraper import get_games
from scrapers.series_scraper import get_all_series

### --- Variables --- ###
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["cbd_speedrun_scraper_test"]

### --- Functions --- ###
def scrape_regions():
    regions_start_time = time.time()

    logging.info("Starting region scraping...")
    region_col = mydb["regions"]
    region_col.drop()
    get_all_regions(region_col)

    regions_end_time = time.time() - regions_start_time
    logging.info(f"Region scraping took {regions_end_time} seconds")
    print(f"Region scraping took {regions_end_time} seconds")

def scrape_platforms():
    platforms_start_time = time.time()

    logging.info("Starting platform scraping...")
    plat_col = mydb["platforms"]
    plat_col.drop()
    get_all_platforms(plat_col)

    platforms_end_time = time.time() - platforms_start_time
    logging.info(f"Platform scraping took {platforms_end_time} seconds")

def scrape_games(offset, MAX_GAME_CALLS, clear_db):
    games_start_time = time.time()
    flag = False

    logging.info("Starting game scraping...")

    game_col = mydb["games"]
    cat_col = mydb["categories"]
    level_col = mydb["levels"]
    var_col = mydb["variables"]

    if clear_db:
        game_col.drop()
        cat_col.drop()
        level_col.drop()
        var_col.drop()


    while not flag:
        flag = get_games(offset, MAX_GAME_CALLS, game_col, cat_col, level_col, var_col)
        offset += MAX_GAME_CALLS

        if offset + MAX_GAME_CALLS > 40000:
            break

    games_end_time = time.time() - games_start_time
    logging.info(f"Game scraping took {games_end_time} seconds")
    print(f"Game scraping took {games_end_time} seconds")

def scrape_series():
    series_start_time = time.time()

    logging.info("Starting series scraping...")
    ser_col = mydb["series"]
    ser_col.drop()
    get_all_series(ser_col)

    series_end_time = time.time() - series_start_time
    logging.info(f"Series scraping took {series_end_time} seconds")