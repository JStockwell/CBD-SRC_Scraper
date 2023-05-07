import requests
import logging

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/regions'
MAX_CALLS = 1000

### --- Utils --- ###

### --- Functions --- ###
def get_all_regions(collection):
    result = []
    i = 0

    while i < 1000:
        region_list = requests.get(f'{URL}?max={MAX_CALLS}&offset={i * MAX_CALLS}').json()

        if "data" not in region_list:
            break
        
        region_list = region_list["data"]

        for region in region_list:
            post = {}

            post["id"] = region["id"]
            post["name"] = region["name"]

            result.append(post)
            
            logging.info(f'Platform scanned: {region["name"]}')
            #print(f'Platform scanned: {region["name"]}')

        if len(region_list) < MAX_CALLS:
            logging.info(f"Regions scanned: {len(result)}")
            #print(f"Regions scanned: {len(result)}")
            break

        i += 1
        logging.info(f"Regions scanned: {i * MAX_CALLS}")
        #print(f"Regions scanned: {i * MAX_CALLS}")

    x = collection.insert_many(result)
    return x.inserted_ids