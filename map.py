COOLATTIN_COORDS = [52.7535, -6.4898]

import folium
import json

class Maps:
    def __init__(self, json_path):
        with open(json_path, encoding="utf-8") as f:
            self.geojson = json.load(f)
            for feature in self.geojson["features"]:
                name_english = feature["properties"]["TL_ENGLISH"]
                link = f'<a href="/townlands/{name_english.title()}" target="_blank">More details</a>'
                feature["properties"]["TL_URL"] = link

    def create_coolattin_map(self):
        map = folium.Map(
            location=COOLATTIN_COORDS,
            prefer_canvas=True,
            zoom_start=10)
        map.width = 500;

        folium.Marker(COOLATTIN_COORDS, popup="Coolattin House").add_to(map)

        folium.GeoJson(
            self.geojson,
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

    def create_map_by_townland(self, townland):
        tl_gjson = self.get_townland_geojson(townland)

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

    def get_townland_geojson(self, townland):
        tl_geojson = None
        for x in self.geojson["features"]:
            if x["properties"]["TL_ENGLISH"] == townland.upper():
                tl_geojson = {
                    "type": "FeatureCollection",
                    "features": [x]
                }
                break
        return tl_geojson
