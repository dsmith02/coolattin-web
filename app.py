import io
import json

from flask import Flask, render_template, send_file
import folium
import pandas as pd
import plotly.graph_objs as go
from population import CensusData
import plotly

json_data = None
census = CensusData("static/data/wicklow-census-data.csv")
tenant_list = "static/data/tenants-merged-11_02_25.csv"

# Loads the geographical JSON data for townlands
def load_json_data():
    global json_data
    json_path = "static/data/townlands.json"
    with open(json_path, encoding="utf-8") as f:
        json_data = json.load(f)


app = Flask(__name__)
load_json_data()

# Folium takes the latitude (y-axis) then the longitude (x-axis)
COOLATTIN_COORDS = [52.7535, -6.4898]


##################
### APP ROUTES ###
##################
@app.route('/')
def index():
    map = create_map()
    map_html = map._repr_html_()
    return render_template("index.html", map_html=map_html)

"""
Loads an individual townland's page. Checks that the townland is contained within the GeoJSON, if not, it returns a blank error page. Otherwise loads the page and map.
"""
@app.route("/townlands/<name>")
def townland(name):
    name = name.title()
    if get_townland_geojson(name) is None:
        return render_template("townland_not_found.html", townland=name)
    else:
        td = census.get_townland_data(name)
        print(td)
        val = td["1841 Male"]
        print(td["1841 Male"][0])
        return render_template("townland.html",
                               townland=name.title(),
                               townland_vrti_link=get_vrti_link(name),
                               tenancies=get_records_for_townland(name),
                               population=int(census.get_townland_data(name)["1841 Male"][0]),
                               map_html=create_map_by_townland(name)._repr_html_())

@app.route("/export/<townland>")
def extract_townland_records(townland):
    df = pd.read_csv("static/data/tenants-merged-test.csv")
    extracted_records = df[df["townland"].str.strip().str.lower() == townland.strip().lower()]

    output = io.StringIO()
    extracted_records.to_csv(output, index=False)

    return send_file(
        io.BytesIO(output.getvalue().encode()),  # Convert to bytes
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"{townland}_extracted.csv"
    )

@app.route("/browse")
def browse():
    return render_template("browse.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/plot")
def plot():
    years = [1830, 1840, 1850, 1860, 1870]
    populations = [120, 150, 100, 80, 60]  # Replace with real data
    fig = go.Figure(data=[go.Bar(x=years, y=populations, marker=dict(color='blue'))])
    fig.update_layout(title=f"Population of TEST Over Time", xaxis_title="Year", yaxis_title="Population")
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("plot.html", graph_json=graph_json, townland_name="TEST")

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
        link = f'<a href="/townlands/{name_english.title()}" target="_blank">More details</a>'
        feature["properties"]["TL_URL"] = link

    folium.GeoJson(
        json_data,
        name="Townlands",
        popup=folium.GeoJsonPopup(
            fields=["TL_ENGLISH", "TL_GAEILGE", "T_POP_1839_", "T_POP_1868", "TL_URL"],
            aliases=["Townland (EN):", "Townland (GA):", "Population (1839):", "Population (1868):", ""],
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
    tl_gjson = get_townland_geojson(townland_name)

    if tl_gjson is None:
        map = folium.Map(
            location=COOLATTIN_COORDS,
            prefer_canvas=True,
            zoom_start=10)
        map.width = 500
        folium.Marker(COOLATTIN_COORDS, popup="Coolattin House").add_to(map)
        return map

    # Centroid = ( SUM OF X-VALUES / N, SUM OF Y-VALUES / N), where N = total number of vertices i.e. no. of X, Y pairs
    # https://www.omnicalculator.com/math/centroid
    # n = tl_gjson["features"][0]["geometry"]["coordinates"][0][0][0]
    # print(f"N = {n}")
    lon_sum = 0
    lat_sum = 0
    for coord in tl_gjson["features"][0]["geometry"]["coordinates"][0]:
        lon_sum += coord[0]
        lat_sum += coord[1]
    centroid_x = lon_sum / len(tl_gjson["features"][0]["geometry"]["coordinates"][0])
    centroid_y = lat_sum / len(tl_gjson["features"][0]["geometry"]["coordinates"][0])

    map = folium.Map(
        location=[centroid_y, centroid_x],
        prefer_canvas=True,
        zoom_start=12)
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

def get_vrti_link(townland):
    townlands = pd.read_csv("static/data/official-aligned.csv")
    for index, row in townlands.iterrows():
        if row.iloc[0] == townland:
            return row.iloc[1]
    return None

def get_records_for_townland(townland):
    records = pd.read_csv(tenant_list)
    townland_records = records[records["townland"].str.strip().str.lower() == townland.lower()]
    return townland_records.to_dict(orient="records")
