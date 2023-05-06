import requests
import logging
import time

def api_call(URL):
    i = 1

    while i < 11:
        request = requests.get(URL).json()

        if "data" not in request:
            if request["status"] == 420:
                logging.warning(f"Too many requests, waiting {i / 10} seconds...")
                print(f"Too many requests, waiting {i / 10} seconds...")
                time.sleep(i / 10)
                i += 1
            
            else:
                print("I broke status")
                break
            
        else:
            break

    if "data" not in request:
        logging.error(request)
        print("ERROR CHECK LOG FILE")
        return None
    
    else:
        return request["data"]