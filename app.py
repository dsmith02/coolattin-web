import json

from flask import Flask, render_template
import folium

app = Flask(__name__)
COOLATTIN_COORDS = [52.7535, -6.4898]
json_data = None

##################
### APP ROUTES ###
##################
@app.route('/')
def index():
    load_json_data()
    map = create_map()
    map_html = map._repr_html_()
    return render_template("index.html", map_html=map_html)

@app.route("/townlands/<name>")
def townland(name):
    return render_template("townland.html", townland=name)

@app.route("/browse")
def browse():
    return render_template("browse.html")

########################
### HELPER FUNCTIONS ###
########################

def check_if_townland_exists(name):
    for tn in json_data["features"]:
        if name == tn:
            return True
    return False

# Create map
def create_map():
    map = folium.Map(
        location=COOLATTIN_COORDS,
        prefer_canvas=True,
        zoom_start=10)
    map.width = 500;

    folium.Marker(COOLATTIN_COORDS, popup="Coolattin House", tooltip="CLICK HERE FOR MORE!").add_to(map)

    folium.GeoJson(
        json_data,
        name="Townlands",
        popup=folium.GeoJsonPopup(
            fields=["TL_ENGLISH", "TL_GAEILGE", "T_POP_1839_", "T_POP_1868"],  # Display these properties
            aliases=["Townland (EN):", "Townland (GA):", "Population (1839):", "Population (1868):"],  # Labels
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

# Loads the geographical JSON data for townlands
def load_json_data():
    global json_data
    json_path = "static/data/townlands.json"
    with open(json_path, encoding="utf-8") as f:
        json_data = json.load(f)

if __name__ == '__main__':
    app.run(debug=True)
