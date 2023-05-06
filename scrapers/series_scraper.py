import requests
import time
import logging

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/series'
MAX_CALLS = 20

### --- Utils --- ###


### --- Functions --- ###

def get_all_series(collection):
    result = []

    i = 0

    while i < 1000:
        c = 0

        while c < 10:
            series = requests.get(f'{URL}?offset={i * MAX_CALLS}').json()

            if "data" not in series:
                if series["status"] == 420:
                    c += 1
                    logging.warning(f"Too many requests, waiting {c} seconds...")
                    print(f"Too many requests, waiting {c} seconds...")
                    time.sleep(c)
                    continue
                
                else:
                    logging.error(f"Error on series. Result len {len(result)}. Saving data...")
                    x = collection.insert_many(result)
                    return x.inserted_ids
                
            else:
                break
        
        series = series["data"]

        for serie in series:
            post = {
                "id": serie["id"],
                "name": serie["names"]["international"],
                "abbreviation": serie["abbreviation"],
                "weblink": serie["weblink"],
                "games": get_serie_games(serie["id"])
            }

            result.append(post)
            logging.info(f"Serie scanned: {serie['names']['international']}")
            print(f"Serie scanned: {serie['names']['international']}")

        if len(series) < MAX_CALLS:
            logging.info(f"Series scanned: {len(result)}")
            print(f"Series scanned: {len(result)}")
            break

        i += 1
        logging.info(f"Series scanned: {i * MAX_CALLS}")
        print(f"Series scanned: {i * MAX_CALLS}")

    x = collection.insert_many(result)
    return x.inserted_ids



def get_serie_games(id):
    result = []

    games = requests.get(f'{URL}/{id}/games').json()

    if "data" not in games:
        return result
    
    for game in games["data"]:
        result.append(game["id"])

    return result