import requests
import logging
import time

def api_call(URL):
    i = 0

    while i < 10:
        request = requests.get(URL).json()

        if "data" not in request:
            if request["status"] == 420:
                i += 1
                logging.warning(f"Too many requests, waiting {i} seconds...")
                print(f"Too many requests, waiting {i} seconds...")
                time.sleep(i)
            
            else:
                break
            
        else:
            break

    if "data" not in request:
        return None
    
    else:
        return request