from flask import Flask, render_template, send_file
from census import CensusData
from townland import TownlandData
from map import Maps
import os

json_data = None
tenant_path = "static/data/tenants-merged-11_02_25.csv"
evictions_path = "static/data/evictions.csv"
emigrations_path = "static/data/emigrations.csv"
tenant_list = "static/data/tenants-merged-11_02_25.csv"
census = CensusData("static/data/wicklow-census-data.csv")
townlands = TownlandData(tenant_path, evictions_path, emigrations_path, "static/data/townlands.json")
maps =  Maps("static/data/townlands.json", townlands)
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
    map = maps.new_create_coolattin_map()
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
        return render_template("townland.html",
                               townland=name.title(),
                               townland_vrti_link=townlands.get_vrti_link(name),
                               tenancies=townlands.get_tenancies(name),
                               pop_graph=census.generate_population_chart(name),
                               population=int(census.get_townland_data(name)["1841 Male"][0]),
                               map_html=maps.create_map_by_townland(name)._repr_html_())

@app.route("/export/<townland>")
def extract_townland_records(townland):
   return send_file(
        townlands.extract_tenancies(townland),
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port)