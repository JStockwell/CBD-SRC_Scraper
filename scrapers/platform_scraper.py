import requests

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/platforms'
MAX_CALLS = 1000

### --- Utils --- ###

### --- Functions --- ###

def get_all_platforms():
    result = {}
    i = 0

    # TODO Change the while loop to 1000. It's 1 for testing
    while i < 1:
        platform_list = requests.get(f'{URL}?max={MAX_CALLS}&offset={i * MAX_CALLS}').json()

        if "data" not in platform_list:
            return result
        
        platform_list = platform_list["data"]

        for platform in platform_list:
            print(f'Platform scanned: {platform["name"]}')
            result[platform["id"]] = {
                "name": platform["name"],
                "released": platform["released"]
            }

        if len(platform_list) < MAX_CALLS:
            print(f"Platforms scanned: {len(result)}")
            break

        i += 1
        print(f"Platforms scanned: {i * MAX_CALLS}")

    return result