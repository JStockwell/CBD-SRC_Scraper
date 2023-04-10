import json

### --- Variables --- ###

json_folder = "json/"

### --- Utils --- ###

def test_write(dictionary, json_name):
    json_object = json.dumps(dictionary, indent=3)
    with open(json_folder + json_name, "w") as outfile:
        outfile.write(json_object)

### --- Functions --- ###
