import json
json_data = None

# Loads the geographical JSON data for townlands
def load_json(path):
    global json_data
    json_path = "static/data/townlands.json"
    with open(path, encoding="utf-8") as f:
        json_data = json.load(f)

# Returns the GeoJSON for a specified townland
def get_townland_geojson(townland_name):
    tl_gjson = None
    for x in json_data["features"]:
        if x["properties"]["TL_ENGLISH"] == townland_name.upper():
            tl_gjson = {
                "type": "FeatureCollection",
                "features": [x]
            }
    return tl_gjson

