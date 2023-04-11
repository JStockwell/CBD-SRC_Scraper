import requests

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/series'
MAX_CALLS = 20

### --- Utils --- ###


### --- Functions --- ###

def get_all_series():
    result = {}

    i = 0

    # TODO Change the while loop to 1000. It's 1 for testing
    while i < 1:
        series = requests.get(f'{URL}?offset={i * MAX_CALLS}').json()

        if "data" not in series:
            return result
        
        series = series["data"]

        for serie in series:
            result[serie["id"]] = {
                "name": serie["names"]["international"],
                "abbreviation": serie["abbreviation"],
                "weblink": serie["weblink"],
                "games": get_serie_games(serie["id"])
            }

            print(f"Serie scanned: {serie['names']['international']}")

        if len(series) < MAX_CALLS:
            print(f"Series scanned: {len(result)}")
            break

        i += 1
        print(f"Series scanned: {i * MAX_CALLS}")

    return result



def get_serie_games(id):
    result = []

    games = requests.get(f'{URL}/{id}/games').json()

    if "data" not in games:
        return result
    
    for game in games["data"]:
        result.append(game["id"])

    return result