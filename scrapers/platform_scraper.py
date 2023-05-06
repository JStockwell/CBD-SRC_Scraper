import requests
import logging

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/platforms'
MAX_CALLS = 1000

### --- Utils --- ###

### --- Functions --- ###

def get_all_platforms(collection):
    result = []
    i = 0

    while i < 1000:
        platform_list = requests.get(f'{URL}?max={MAX_CALLS}&offset={i * MAX_CALLS}').json()

        if "data" not in platform_list:
            break
        
        platform_list = platform_list["data"]

        for platform in platform_list:
            post = {}

            post["id"] = platform["id"]
            post["name"] = platform["name"]
            post["released"] = platform["released"]

            result.append(post)

            logging.info(f'Platform scanned: {platform["name"]}')
            print(f'Platform scanned: {platform["name"]}')

        if len(platform_list) < MAX_CALLS:
            logging.info(f"Platforms scanned: {len(result)}")
            print(f"Platforms scanned: {len(result)}")
            break

        i += 1
        logging.info(f"Platforms scanned: {i * MAX_CALLS}")
        print(f"Platforms scanned: {i * MAX_CALLS}")

    x = collection.insert_many(result)
    return x.inserted_ids