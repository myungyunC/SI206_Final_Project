import json

# All JSON related functions are kept here.

CACHE_FILENAME = "helpers.json"

def read_cache():
    """Reads from the JSON file. Returns an empty dictionary if non-existent."""
    try:
        cache_file = open(CACHE_FILENAME, 'r', encoding="utf-8")
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
        return cache_dict
    except:
        cache_dict = {}
        return cache_dict

def write_cache(cache_dict):
    """Write to the JSON file. Overwrite the file."""
    try:
        with open(CACHE_FILENAME, 'w', encoding="utf-8") as cache_file:
            cache_file.write(json.dumps(cache_dict))
    except:
        print("error when executing write_cache()")

