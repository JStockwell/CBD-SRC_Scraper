from utils.test_utils import test_write
from scrapers.game_scraper import get_all_games
from scrapers.platform_scraper import get_all_platforms

### --- Variables --- ###


### --- Utils --- ###


### --- Functions --- ###


### --- Executions --- ###

print("Starting games test...")
test_write(get_all_games(), "test_games.json")
print("\nStarting platforms test...")
test_write(get_all_platforms(), "test_platforms.json")

# Object type list:
# Game: id, name, weblink, release-date, platforms
# Platform: id, name, released