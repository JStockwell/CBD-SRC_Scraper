import requests

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/regions'

### --- Utils --- ###

### --- Functions --- ###

def get_all_regions():
    result = {}
    i = 0

    while i < 1:
        region_list = requests.get(f'{URL}?max=1000&offset={i * 1000}').json()["data"]

        for region in region_list:
            result[region["id"]] = {
                "name": region["name"]
            }
            print(f'Platform scanned: {region["name"]}')

        if len(region_list) < 1000:
            print(f"Regions scanned: {len(result)}")
            break

        i += 1
        print(f"Regions scanned: {i * 1000}")

    return result