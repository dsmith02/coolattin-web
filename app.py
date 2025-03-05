import io
import json

from flask import Flask, render_template, send_file
import folium
import pandas as pd
from census import CensusData
from townland import TownlandData
from map import Maps

json_data = None
tenant_path = "static/data/tenants-merged-11_02_25.csv"
tenant_list = "static/data/tenants-merged-11_02_25.csv"
census = CensusData("static/data/wicklow-census-data.csv")
townlands = TownlandData(tenant_path, tenant_path, tenant_path, "static/data/townlands.json")
maps =  Maps("static/data/townlands.json")
app = Flask(__name__)

##################
### APP ROUTES ###
##################
@app.route("/")
def index():
    map = maps.create_coolattin_map()
    map_html = map._repr_html_()
    return render_template("index.html", map_html=map_html)

@app.route("/new")
def new():
    map = maps.create_coolattin_map()
    map_html = map._repr_html_()
    return render_template("new.html", map_html=map_html)

"""
Loads an individual townland's page. Checks that the townland is contained within the GeoJSON, if not, it returns a blank error page. Otherwise loads the page and map.
"""
@app.route("/townlands/<name>")
def townland(name):
    name = name.title()
    if townlands.get_townland_geojson(name) is None:
        return render_template("townland_not_found.html", townland=name)
    else:
        td = census.get_townland_data(name)
        print(td)
        val = td["1841 Male"]
        print(td["1841 Male"][0])
        return render_template("townland.html",
                               townland=name.title(),
                               townland_vrti_link=townlands.get_vrti_link(name),
                               tenancies=get_records_for_townland(name),
                               pop_graph=census.generate_population_chart(name),
                               population=int(census.get_townland_data(name)["1841 Male"][0]),
                               map_html=maps.create_map_by_townland(name)._repr_html_())

@app.route("/export/<townland>")
def extract_townland_records(townland):
   return send_file(
        io.BytesIO(townlands.extract_tenancies(townland)),  # Convert to bytes
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"{townland}_tenancies_extracted.csv"
    )

@app.route("/browse")
def browse():
    return render_template("browse.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/plot/<townland>")
def plot_test(townland):
    return render_template("plot.html", graph_json=census.generate_population_chart(townland), townland_name=townland)

########################
### HELPER FUNCTIONS ###
########################
def get_records_for_townland(townland):
    records = pd.read_csv(tenant_list)
    townland_records = records[records["townland"].str.strip().str.lower() == townland.lower()]
    return townland_records.to_dict(orient="records")
