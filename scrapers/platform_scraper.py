import requests

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/platforms'

### --- Utils --- ###

### --- Functions --- ###

def get_all_platforms():
    result = {}
    i = 0

    while i < 1:
        platform_list = requests.get(f'{URL}?max=1000&offset={i * 1000}').json()["data"]

        for platform in platform_list:
            print(f'Platform scanned: {platform["name"]}')
            result[platform["id"]] = {
                "name": platform["name"],
                "released": platform["released"]
            }

        if len(platform_list) < 1000:
            print(f"Platforms scanned: {len(result)}")
            break

        i += 1
        print(f"Games scanned: {i * 1000}")

    return result