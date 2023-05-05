import requests
import time
import logging

### --- Variables --- ###

LEVEL_URL = 'https://speedrun.com/api/v1/levels'
GAME_URL = 'https://speedrun.com/api/v1/games'
MAX_CALLS = 1000

### --- Utils --- ###

### --- Functions --- ###

# Step 1 & 3: Get all games, with ID, name and weblink with extra info
def get_all_games(game_collection, category_collection, level_collection, variable_collection):
    result = []
    i = 0

    while i < 1000:
        c = 0

        while c < 10:
            bulk_games = requests.get(f'{GAME_URL}?_bulk=yes&max={MAX_CALLS}&offset={i * MAX_CALLS}').json()

            if "data" not in bulk_games:
                if bulk_games["status"] == 420:
                    logging.warning("Too many requests, waiting 5 seconds...")
                    print("Too many requests, waiting 5 seconds...")
                    time.sleep(c)
                    c += 1
                    continue
                
                else:
                    logging.error(f"Error on games. Result len {len(result)}. Saving data...")
                    x = game_collection.insert_many(result)
                    return x.inserted_ids
                
            else:
                break
        
        bulk_games = bulk_games["data"]

        j = 0
        for game in bulk_games:
            result.append(get_game(game["id"], category_collection, level_collection, variable_collection))
            j += 1

            if j % 100 == 0:
                logging.info(f"Games scanned: {i * MAX_CALLS + j}")
                print(f"Games scanned: {i * MAX_CALLS + j}")
            
        if len(bulk_games) < MAX_CALLS:
            logging.info(f"Games scanned: {len(result)}")
            print(f"Games scanned: {len(result)}")
            break

        i += 1
        logging.info(f"Games scanned: {i * MAX_CALLS}")
        print(f"Games scanned: {i * MAX_CALLS}")

    x = game_collection.insert_many(result)
    return x.inserted_ids

# Step 2: Get the information for a single game
def get_game(game_id, category_collection, level_collection, variable_collection):
    result = {}
    game = requests.get(f'{GAME_URL}/{game_id}').json()

    if "data" not in game:
        return result

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
        categories = requests.get(f'{LEVEL_URL}/{ids[1]}/categories?embed=variables').json()
    else:
        categories = requests.get(f'{GAME_URL}/{ids[0]}/categories?embed=variables').json()

    if "data" not in categories:
        return result

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
    levels = requests.get(f'{GAME_URL}/{game_id}/levels').json()

    if "data" not in levels:
        return result
    
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