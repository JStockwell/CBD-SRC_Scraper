import requests

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/regions'
MAX_CALLS = 1000

### --- Utils --- ###

### --- Functions --- ###

def get_all_regions():
    result = {}
    i = 0

    while i < 1:
        region_list = requests.get(f'{URL}?max={MAX_CALLS}&offset={i * MAX_CALLS}').json()

        if "data" not in region_list:
            return result
        
        region_list = region_list["data"]

        for region in region_list:
            result[region["id"]] = {
                "name": region["name"]
            }
            print(f'Platform scanned: {region["name"]}')

        if len(region_list) < MAX_CALLS:
            print(f"Regions scanned: {len(result)}")
            break

        i += 1
        print(f"Regions scanned: {i * MAX_CALLS}")

    return result