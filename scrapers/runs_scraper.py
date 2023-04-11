import requests

### --- Variables --- ###

URL = 'https://speedrun.com/api/v1/runs'
# TODO Change the max to 1000. It's 20 for testing
MAX_CALLS = 200

### --- Utils --- ###

### --- Functions --- ###

# TODO Save users from the run
# !TODO Get runs per leaderboard, per game is too many runs lmao and pagination doesn't work
def get_all_runs():
    result = {}

    i = 0

    # TODO Change the while loop to 1000. It's 1 for testing
    while i < 1000:
        runs = requests.get(f'{URL}?max={MAX_CALLS}&offset={i * MAX_CALLS}').json()

        if "data" not in runs:
            return result
        
        runs = runs["data"]

        for run in runs:
            result[run["id"]] = {
                "game": run["game"],
                "category": run["category"],
                "system": run["system"],
                "time": run["times"],
                "players": get_runs_players(run["players"]),
                "date": run["date"],
                "weblink": run["weblink"],
                "status": run["status"],
                "values": run["values"]
            }

            print(f"Run scanned: {run['id']}")

        if len(runs) < MAX_CALLS:
            print(f"Runs scanned: {len(result)}")
            break

        i += 1
        print(f"Runs scanned: {i * MAX_CALLS}")

    return result

def get_runs_players(players):
    result = []

    for player in players:
        if player["rel"] == "guest":
            result.append(f'GUEST-{player["name"]}')
        else:
            result.append(player["id"])

    return result
