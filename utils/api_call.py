import requests
import logging
import time

def api_call(URL):
    i = 0

    while i < 101:
        request = requests.get(URL).json()

        if "data" not in request:
            if request["status"] == 420:
                if i % 10 == 0 or i == 0:
                    logging.warning(f"Too many requests, trying again...")
                    #print(f"Too many requests, trying again...")
                i += 1
            
            else:
                break
            
        else:
            break

    if "data" not in request:
        logging.error(request)
        print("ERROR CHECK LOG FILE")
        return None
    
    else:
        return request["data"]