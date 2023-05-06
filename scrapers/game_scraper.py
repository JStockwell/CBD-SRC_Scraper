import requests
import time
import logging

from utils.api_call import api_call

### --- Variables --- ###

LEVEL_URL = 'https://speedrun.com/api/v1/levels'
GAME_URL = 'https://speedrun.com/api/v1/games'

### --- Utils --- ###

### --- Functions --- ###

# Step 1 & 3: Get all games, with ID, name and weblink with extra info
def get_games(offset, MAX_GAME_CALLS, game_collection, category_collection, level_collection, variable_collection):
    result = []
    flag = False

    bulk_games = api_call(f'{GAME_URL}?_bulk=yes&max={MAX_GAME_CALLS}&offset={offset}')

    if bulk_games is None:
        logging.error(f"Error on games. Number {offset}. Saving data...")
        return True
    
    bulk_games = bulk_games["data"]

    j = 0
    for game in bulk_games:
        result.append(get_game(game["id"], category_collection, level_collection, variable_collection))
        j += 1

        if j % 100 == 0:
            logging.info(f"Games scanned: {offset + j}")
            print(f"Games scanned: {offset + j}")

    if len(bulk_games) < MAX_GAME_CALLS:
        logging.info(f"Games scanned: {offset + len(bulk_games)}")
        print(f"Games scanned: {offset + len(bulk_games)}")
        flag = True

    else:
        logging.info(f"Games scanned: {offset + MAX_GAME_CALLS}")
        print(f"Games scanned: {offset + MAX_GAME_CALLS}")

    x = game_collection.insert_many(result)
    return flag

# Step 2: Get the information for a single game
def get_game(game_id, category_collection, level_collection, variable_collection):
    result = {}

    game = api_call(f'{GAME_URL}/{game_id}')

    if game is None:
        logging.error(f"Error on game {game_id}")
        return {"id": game_id, "error": True}

    game = game["data"]

    result = {
        "id": game["id"],
        "name": game["names"]["international"],
        "weblink": game["weblink"],
        "release-date": game["release-date"],
        "platforms": game["platforms"],
        "regions": game["regions"]
    }

    get_levels(game_id, level_collection, category_collection, variable_collection)
    get_categories([game_id,None], False, category_collection, variable_collection)
    logging.info(f"Game scanned: {game['names']['international']}")
    print(f"Game scanned: {game['names']['international']}")
    return result

# Step 4: Get all categories for a single game
def get_categories(ids, level_flag, collection, variable_collection):
    result = []
    category_ids = []

    if level_flag:
        categories = api_call(f'{LEVEL_URL}/{ids[1]}/categories?embed=variables')
    else:
        categories = api_call(f'{GAME_URL}/{ids[0]}/categories?embed=variables')

    if categories is None:
        if level_flag:
            return{"id": ids[1], "error": True}
        else:
            return{"id": ids[0], "error": True}

    categories = categories["data"]
    for category in categories:
        post = {
            "id": category["id"],
            "game": ids[0],
            "level": ids[1],
            "name": category["name"],
            "weblink": category["weblink"],
            "type": category["type"],
            "rules": category["rules"],
        }

        result.append(post)
        category_ids.append(category["id"])
        format_variables(category["variables"]["data"], variable_collection)
        logging.info(f"Category scanned: {category['name']}")
        print(f"Category scanned: {category['name']}")

    if len(result) > 0:
        x = collection.insert_many(result)
        return x.inserted_ids
    else:
        return "No categories found"

# Step 4.5 & 5.5: Format the variables for a single game
def format_variables(variables, collection):
    result = []

    for variable in variables:
        post = {
            "id": variable["id"],
            "category": variable["category"],
            "name": variable["name"],
            "scope": variable["scope"],
            "mandatory": variable["mandatory"],
            "values": variable["values"]["values"],
            "is-subcategory": variable["is-subcategory"]
        }

        result.append(post)
        logging.info(f"Variable scanned: {variable['name']}")
        print(f"Variable scanned: {variable['name']}")

    if len(result) > 0:
        x = collection.insert_many(result)
        return x.inserted_ids
    
    else:
        return "No variables found"

# Step 5: Get all levels for a single game
def get_levels(game_id, collection, category_collection, variable_collection):
    result = []

    levels = api_call(f'{GAME_URL}/{game_id}/levels')

    if levels is None:
        return {"id": game_id, "error": True}
    
    levels = levels["data"]

    for level in levels:
        post = {
            "id": level["id"],
            "game": game_id,
            "name": level["name"],
            "weblink": level["weblink"],
            "rules": level["rules"],
        }

        get_categories([game_id, level["id"]], True, category_collection, variable_collection)
        result.append(post)
        logging.info(f"Level scanned: {level['name']}")
        print(f"Level scanned: {level['name']}")

    if len(result) > 0:
        x = collection.insert_many(result)
        return x.inserted_ids
    else:
        return "No levels found"