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

    folium.Marker(COOLATTIN_COORDS, popup="Coolattin House", tooltip="Click me!").add_to(map)

    geojson_path = "static/data/townlands.json"
    with open(geojson_path, encoding="utf-8") as f:
        folium.GeoJson(f.read(), name="Townlands").add_to(map)

    # Generate the map HTML
    map_to_html = map._repr_html_()

    return render_template("index.html", map_html=map_to_html)

if __name__ == '__main__':
    app.run(debug=True)
