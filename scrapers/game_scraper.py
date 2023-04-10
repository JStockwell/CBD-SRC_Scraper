import requests

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/games'

### --- Utils --- ###

### --- Functions --- ###

# Step 2: Get the information for a single game
# Information to save: ID, name, weblink, release date, platforms
def get_game(game_id):
    result = {}
    game = requests.get(f'{URL}/{game_id}').json()["data"]

    result = {
        "name": game["names"]["international"],
        "weblink": game["weblink"],
        "release-date": game["release-date"],
        "platforms": game["platforms"]
    }

    print(f"Games scanned: {game['names']['international']}")
    return result

# Step 1 & 3: Get all games, with ID, name and weblink with extra info
def get_all_games():
    result = {}
    i = 0

    # TODO Change the while loop to 1000. It's 1 for testing
    while i < 1:
        # TODO Change the max to 1000. It's 20 for testing
        bulk_games = requests.get(f'{URL}?_bulk=yes&max=20&offset={i * 1000}').json()["data"]
        for game in bulk_games:
            result[game["id"]] = get_game(game["id"])
            
        if len(bulk_games) < 1000:
            print(f"Games scanned: {len(result)}")
            break

        i += 1
        print(f"Games scanned: {i * 1000}")

    return result