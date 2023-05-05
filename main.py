import time

from utils.test_utils import test_write
from scrapers.game_scraper import get_all_games, get_game, get_categories, get_levels
from scrapers.platform_scraper import get_all_platforms
from scrapers.region_scraper import get_all_regions
from scrapers.series_scraper import get_all_series
from scrapers.runs_scraper import get_all_runs

### --- Variables --- ###


### --- Utils --- ###


### --- Functions --- ###


### --- Executions --- ###

categories_start_time = time.time()
print("\nStarting categories test...")
test_write(get_categories("y6545p8d", False), "test_categories.json")
categories_end_time = time.time() - categories_start_time

levels_start_time = time.time()
print("\nStarting levels test...")
test_write(get_levels("y6545p8d"), "test_levels.json")
levels_end_time = time.time() - levels_start_time

game_start_time = time.time()
print("Starting individual game test...")
test_write(get_game("o1yrkr6q"), "test_game.json")
game_end_time = time.time() - game_start_time

games_start_time = time.time()
print("\nStarting games test...")
#test_write(get_all_games(), "test_games.json")
games_end_time = time.time() - games_start_time

platform_start_time = time.time()
print("\nStarting platforms test...")
test_write(get_all_platforms(), "test_platforms.json")
platform_end_time = time.time() - platform_start_time

region_start_time = time.time()
print("\nStarting regions test...")
test_write(get_all_regions(), "test_regions.json")
region_end_time = time.time() - region_start_time

series_start_time = time.time()
print("\nStarting series test...")
test_write(get_all_series(), "test_series.json")
series_end_time = time.time() - series_start_time

runs_start_time = time.time()
print("\nStarting runs test...")
#test_write(get_all_runs(), "test_runs.json")
runs_end_time = time.time() - runs_start_time

print("\n")
print(f"Categories test took {categories_end_time} seconds")
print(f"Levels test took {levels_end_time} seconds")
print(f"Game test took {game_end_time} seconds")
print(f"Games test took {games_end_time} seconds")
print(f"Platforms test took {platform_end_time} seconds")
print(f"Regions test took {region_end_time} seconds")
print(f"Series test took {series_end_time} seconds")

# Object type list:

# Game: id, name, weblink, release-date, platforms*, regions*, cateogies, levels
### Category: id, name, weblink, type, rules, variables
##### Variable: id, name, scope, mandatory, values, is-subcategory
### Level: id, name, weblink, variables
##### Variable: id, name, scope, mandatory, values, is-subcategory

# Platform: id, name, released
# Region: id, name
# Series: id, name, weblink, released, games