import json

from flask import Flask, render_template
import folium

json_data = None


# Loads the geographical JSON data for townlands
def load_json_data():
    global json_data
    json_path = "static/data/townlands.json"
    with open(json_path, encoding="utf-8") as f:
        json_data = json.load(f)


app = Flask(__name__)
load_json_data()
COOLATTIN_COORDS = [52.7535, -6.4898]


##################
### APP ROUTES ###
##################
@app.route('/')
def index():
    map = create_map()
    map_html = map._repr_html_()
    return render_template("index.html", map_html=map_html)


@app.route("/townlands/<name>")
def townland(name):
    return render_template("townland.html", townland=name, map_html=create_map_by_townland(name)._repr_html_())


@app.route("/browse")
def browse():
    return render_template("browse.html")


@app.route("/about")
def about():
    return render_template("about.html")


########################
### HELPER FUNCTIONS ###
########################

# Create map
def create_map():
    map = folium.Map(
        location=COOLATTIN_COORDS,
        prefer_canvas=True,
        zoom_start=10)
    map.width = 500;

    folium.Marker(COOLATTIN_COORDS, popup="Coolattin House").add_to(map)

    for feature in json_data["features"]:
        name_english = feature["properties"]["TL_ENGLISH"]
        link = f'<a href="/townlands/{name_english.replace(" ", "-").capitalize()}" target="_blank">More details</a>'
        feature["properties"]["TL_URL"] = link  # Add the link as a new property

    folium.GeoJson(
        json_data,
        name="Townlands",
        popup=folium.GeoJsonPopup(
            fields=["TL_ENGLISH", "TL_GAEILGE", "T_POP_1839_", "T_POP_1868", "TL_URL"],  # Display these properties
            aliases=["Townland (EN):", "Townland (GA):", "Population (1839):", "Population (1868):", ""],  # Labels
            localize=True  # Automatically format numbers if needed
        ),
        tooltip=folium.GeoJsonTooltip(
            fields=["TL_ENGLISH"],  # Show the townland name on hover
            aliases=["Townland:"],
            sticky=True
        ),
        style_function=lambda feature: {
            "fillColor": "#7fd4db",  # Default fill color for polygons
            "color": "black",  # Outline color
            "weight": 1.5,  # Border thickness
            "fillOpacity": 0.4  # Transparency of fill color
        },
        zoom_on_click=False
    ).add_to(map)

    return map

"""
Gets the townlands geojson data
"""
def get_townland_geojson(townland_name):
    tl_gjson = None
    for x in json_data["features"]:
        if x["properties"]["TL_ENGLISH"] == townland_name.upper():
            tl_gjson = {
                "type": "FeatureCollection",
                "features": [x]
            }
    return tl_gjson

def create_map_by_townland(townland_name):
    tl_gjson = None
    for x in json_data["features"]:
        if x["properties"]["TL_ENGLISH"] == townland_name.upper():

            tl_gjson = {
                "type": "FeatureCollection",
                "features": [x]
            }

    if tl_gjson is None:
        map = folium.Map(
            location=COOLATTIN_COORDS,
            prefer_canvas=True,
            zoom_start=10)
        map.width = 500
        folium.Marker(COOLATTIN_COORDS, popup="Coolattin House").add_to(map)
        return map

    print(tl_gjson)
    map = folium.Map(
        location=COOLATTIN_COORDS,
        prefer_canvas=True,
        zoom_start=10)
    map.width = 500

    folium.GeoJson(
        tl_gjson,
        name="Specific townland",
        popup=folium.GeoJsonPopup(
            fields=["TL_ENGLISH", "TL_GAEILGE", "T_POP_1839_", "T_POP_1868"],
            aliases=["Townland (EN):", "Townland (GA):", "Population (1839):", "Population (1868):"],
            localize=True
        ),
        tooltip=folium.GeoJsonTooltip(
            fields=["TL_ENGLISH"],
            aliases=["Townland:"],
            sticky=True
        ),
        style_function=lambda feature: {
            "fillColor": "#7fd4db",
            "color": "black",
            "weight": 1.5,
            "fillOpacity": 0.4
        },
        zoom_on_click=False
    ).add_to(map)

    return map
