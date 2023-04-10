from scrapers.game_scraper import get_all_games
from utils.test_utils import test_write

### --- Variables --- ###


### --- Utils --- ###


### --- Functions --- ###


### --- Executions --- ###

test_write(get_all_games(), "test_games.json")