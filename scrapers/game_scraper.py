import requests

### --- Variables --- ###

LEVEL_URL = 'https://speedrun.com/api/v1/levels'
GAME_URL = 'https://speedrun.com/api/v1/games'

### --- Utils --- ###

### --- Functions --- ###

# Step 1 & 3: Get all games, with ID, name and weblink with extra info
def get_all_games():
    result = {}
    i = 0

    # TODO Change the while loop to 1000. It's 1 for testing
    while i < 1:
        # TODO Change the max to 1000. It's 20 for testing
        bulk_games = requests.get(f'{GAME_URL}?_bulk=yes&max=20&offset={i * 1000}').json()["data"]

        c = 0
        for game in bulk_games:
            result[game["id"]] = get_game(game["id"])
            c += 1

            if c % 100 == 0:
                print(f"Games scanned: {i * 1000 + c}")
            
        if len(bulk_games) < 1000:
            print(f"Games scanned: {i * 1000 + len(result)}")
            break

        i += 1
        print(f"Games scanned: {i * 1000}")

    return result

# Step 2: Get the information for a single game
def get_game(game_id):
    result = {}
    game = requests.get(f'{GAME_URL}/{game_id}').json()

    if "data" not in game:
        return result

    game = game["data"]
    categories = get_categories(game_id, False)

    result = {
        "name": game["names"]["international"],
        "weblink": game["weblink"],
        "release-date": game["release-date"],
        "platforms": game["platforms"],
        "regions": game["regions"],
        "categories": categories,
        "levels": get_levels(game_id)
    }

    print(f"Game scanned: {game['names']['international']}")
    return result

# Step 4: Get all categories for a single game
def get_categories(id, level_flag):
    result = {}
    if level_flag:
        categories = requests.get(f'{LEVEL_URL}/{id}/categories?embed=variables').json()
    else:
        categories = requests.get(f'{GAME_URL}/{id}/categories?embed=variables').json()

    if "data" not in categories:
        return result

    categories = categories["data"]
    for category in categories:
        result[category["id"]] = {
            "name": category["name"],
            "weblink": category["weblink"],
            "type": category["type"],
            "rules": category["rules"],
            "variables": format_variables(category["variables"]["data"])
        }
        print(f"Category scanned: {category['name']}")

    return result

# Step 4.5 & 5.5: Format the variables for a single game
def format_variables(variables):
    result = {}

    for variable in variables:
        result[variable["id"]] = {
            "name": variable["name"],
            "scope": variable["scope"],
            "mandatory": variable["mandatory"],
            "values": variable["values"]["values"],
            "is-subcategory": variable["is-subcategory"]
        }

        print(f"Variable scanned: {variable['name']}")

    return result

# Step 5: Get all levels for a single game
def get_levels(game_id):
    result = {}
    levels = requests.get(f'{GAME_URL}/{game_id}/levels').json()

    if "data" not in levels:
        return result
    
    levels = levels["data"]

    for level in levels:
        result[level["id"]] = {
            "name": level["name"],
            "weblink": level["weblink"],
            "rules": level["rules"],
            "categories": get_categories(level["id"], True)
        }
        print(f"Level scanned: {level['name']}")

    return result