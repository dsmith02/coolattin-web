import json

from flask import Flask, render_template
import folium
import requests

app = Flask(__name__)

COOLATTIN_COORDS = [52.7535, -6.4898]


@app.route('/')
def index():
    map = folium.Map(
        location=COOLATTIN_COORDS,
        prefer_canvas=True,
        zoom_start=10)
    map.width = 500;

    folium.Marker(COOLATTIN_COORDS, popup="Coolattin House", tooltip="Click me!").add_to(map)

    json_path = "static/data/townlands.json"
    json_data = None

    # Load the GeoJSON and add popups using TL_ENGLISH (townland name in English)
    with open(json_path, encoding="utf-8") as f:
        json_data = json.load(f)

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
            "fillColor": "red",  # Default fill color for polygons
            "color": "black",  # Outline color
            "weight": 1.5,  # Border thickness
            "fillOpacity": 0.4  # Transparency of fill color
        },
        zoom_on_click=True
    ).add_to(map)

    # Generate the map HTML
    map_to_html = map._repr_html_()

    return render_template("index.html", map_html=map_to_html)


@app.route("/browse")
def browse():
    return f"""<h1>HELLO</h1>"""


if __name__ == '__main__':
    app.run(debug=True)
