import copy

COOLATTIN_COORDS = [52.7535, -6.4898]

import folium
import json


class Maps:
    def __init__(self, json_path, townlands):
        with open(json_path, encoding="utf-8") as f:
            self.geojson = json.load(f)
            for feature in self.geojson["features"]:
                name_english = feature["properties"]["TL_ENGLISH"]
                link = f'<a href="/townlands/{name_english.title()}" target="_blank">More details</a>'
                feature["properties"]["TL_URL"] = link
        self.townlands = townlands

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

        self.new_create_coolattin_map()

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

        centroid_x, centroid_y = self.calculate_centroid(townland)

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

    def new_create_coolattin_map(self):
        map = folium.Map(
            location=COOLATTIN_COORDS,
            prefer_canvas=True,
            tiles=None,
            zoom_start=10)
        map.width = 500

        folium.TileLayer("OpenStreetMap", name="Base").add_to(map)

        folium.Marker(COOLATTIN_COORDS, popup="Coolattin House").add_to(map)

        townlands_layer = folium.FeatureGroup(name="Townlands", show=True)
        evictions_layer = folium.FeatureGroup(name="Evictions", show=False)
        emigrations_layer = folium.FeatureGroup(name="Emigrations", show=False)

        folium.GeoJson(
            self.geojson,
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
            }).add_to(townlands_layer)

        for feature in self.geojson["features"]:
            name = feature["properties"]["TL_ENGLISH"]
            # print(f"Checking {name}")
            if len(self.townlands.get_evictions(name)) > 0:
                folium.GeoJson(
                    feature,
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
                        "fillColor": "#e66750",
                        "color": "black",
                        "weight": 1.5,
                        "fillOpacity": 0.4
                    }).add_to(evictions_layer)

            if len(self.townlands.get_emigrations(name)) > 0:
                folium.GeoJson(
                    feature,
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
                        "fillColor": "#e6e650",
                        "color": "black",
                        "weight": 1.5,
                        "fillOpacity": 0.4
                    }).add_to(emigrations_layer)

        townlands_layer.add_to(map)
        evictions_layer.add_to(map)
        emigrations_layer.add_to(map)

        folium.LayerControl().add_to(map)
        return map

    def create_map_with_heatmap(self):
        map = folium.Map(
            location=COOLATTIN_COORDS,
            prefer_canvas=True,
            tiles=None,
            zoom_start=10)
        map.width = 500

        folium.TileLayer("OpenStreetMap", name="Base").add_to(map)
        folium.Marker(COOLATTIN_COORDS, popup="Coolattin House").add_to(map)

        townlands_layer = folium.FeatureGroup(name="Townlands", show=True)
        tenancies_layer = folium.FeatureGroup(name="Tenancies Heat Map", show=False)
        evictions_layer = folium.FeatureGroup(name="Evictions Heat Map", show=False)
        emigrations_layer = folium.FeatureGroup(name="Emigrations Heat Map", show=False)

        from branca.colormap import LinearColormap

        colormap = LinearColormap(
            ['#fff27a', '#fcc538', '#e80000'],
            vmin=0,
            vmax=120
        )

        folium.GeoJson(
            self.geojson,
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
            }).add_to(townlands_layer)

        for feature in self.geojson["features"]:
            name = feature["properties"]["TL_ENGLISH"]
            centroid_x, centroid_y = self.calculate_centroid(name)
            folium.map.Marker(
                location=[centroid_y, centroid_x],
                icon=folium.DivIcon(
                    icon_size=(150,36),
                    icon_anchor=(75,18),
                    html=f"<div style='font-size: 2; px; color: black; text-align: center; white-space: nowrap;'>{name}</div>"
                )
            ).add_to(map)

            tenancies_count = len(self.townlands.get_tenancies(name)) if hasattr(self.townlands, 'get_tenancies') else 0
            if tenancies_count > 0:
                popup_html = f"""
                    <div>
                        <h4>{name}</h4>
                        <p>Tenancies: {tenancies_count}</p>
                        <p>Population (1839): {feature['properties']['T_POP_1839_']}</p>
                        <p>Population (1868): {feature['properties']['T_POP_1868']}</p>
                    </div>
                    """

                folium.GeoJson(
                    feature,
                    popup=folium.Popup(popup_html),
                    tooltip=folium.GeoJsonTooltip(
                        fields=["TL_ENGLISH"],
                        aliases=["Townland:"],
                        sticky=True
                    ),
                    style_function=lambda x, count=tenancies_count: {
                        "fillColor": colormap(count),
                        "color": "black",
                        "weight": 1.5,
                        "fillOpacity": 0.7
                    }).add_to(tenancies_layer)

            evictions_count = len(self.townlands.get_evictions(name))
            if evictions_count > 0:
                popup_html = f"""
                    <div>
                        <h4>{name}</h4>
                        <p>Evictions: {evictions_count}</p>
                        <p>Population (1839): {feature['properties']['T_POP_1839_']}</p>
                        <p>Population (1868): {feature['properties']['T_POP_1868']}</p>
                    </div>
                    """

                folium.GeoJson(
                    feature,
                    popup=folium.Popup(popup_html),
                    tooltip=folium.GeoJsonTooltip(
                        fields=["TL_ENGLISH"],
                        aliases=["Townland:"],
                        sticky=True
                    ),
                    style_function=lambda x, count=evictions_count: {
                        "fillColor": colormap(count),
                        "color": "black",
                        "weight": 1.5,
                        "fillOpacity": 0.7
                    }).add_to(evictions_layer)

            emigrations_count = len(self.townlands.get_emigrations(name))
            if emigrations_count > 0:
                popup_html = f"""
                    <div>
                        <h4>{name}</h4>
                        <p>Emigrations: {emigrations_count}</p>
                        <p>Population (1839): {feature['properties']['T_POP_1839_']}</p>
                        <p>Population (1868): {feature['properties']['T_POP_1868']}</p>
                    </div>
                    """

                folium.GeoJson(
                    feature,
                    popup=folium.Popup(popup_html),
                    tooltip=folium.GeoJsonTooltip(
                        fields=["TL_ENGLISH"],
                        aliases=[f"Townland:"],
                        sticky=True
                    ),
                    style_function=lambda x, count=emigrations_count: {
                        "fillColor": colormap(count),
                        "color": "black",
                        "weight": 1.5,
                        "fillOpacity": 0.7
                    }).add_to(emigrations_layer)

        # folium.GeoJson(
        #     self.geojson,
        #     style_function=lambda x: {
        #         'fillOpacity': 0,
        #         'color': 'none'
        #     },
        #     tooltip=folium.GeoJsonTooltip(
        #         fields=["TL_ENGLISH"],
        #         aliases=["Townland:"],
        #         sticky=True
        #     ),
        #     popup=folium.GeoJsonPopup(
        #         fields=["TL_ENGLISH"],
        #         aliases=["Townland:"],
        #         sticky=True
        #     ),
        #     highlight_function=lambda x: {'weight': 2, 'color': 'blue'},
        #     name='Townland Labels'
        # ).add_to(townlands_layer)

        townlands_layer.add_to(map)
        tenancies_layer.add_to(map)
        evictions_layer.add_to(map)
        emigrations_layer.add_to(map)

        folium.LayerControl().add_to(map)

        legend_html = """
            <div id="legend" style="position: fixed; bottom: 50px; left: 10px; z-index:9999; font-size:12px; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
                <h4 style="margin: 0 0 5px 0;">Distribution</h4>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="background: #fff27a; width: 15px; height: 15px; margin-right: 5px;"></div>
                    <div>Low (1-50)</div>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="background: #fcc538; width: 15px; height: 15px; margin-right: 5px;"></div>
                    <div>Medium (51-120)</div>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="background: #e80000; width: 15px; height: 15px; margin-right: 5px;"></div>
                    <div>High (>120)</div>
                </div>
            </div>
            """

        map.get_root().html.add_child(folium.Element(legend_html))

        return map

    def calculate_centroid(self, townland):
        # Centroid = ( SUM OF X-VALUES / N, SUM OF Y-VALUES / N), where N = total number of vertices i.e. no. of X, Y pairs
        # https://www.omnicalculator.com/math/centroid
        tl_gjson = self.get_townland_geojson(townland)

        if tl_gjson is None:
            return 0, 0

        lon_sum = 0
        lat_sum = 0
        for coord in tl_gjson["features"][0]["geometry"]["coordinates"][0]:
            lon_sum += coord[0]
            lat_sum += coord[1]
        centroid_x = lon_sum / len(tl_gjson["features"][0]["geometry"]["coordinates"][0])
        centroid_y = lat_sum / len(tl_gjson["features"][0]["geometry"]["coordinates"][0])
        return centroid_x, centroid_y
