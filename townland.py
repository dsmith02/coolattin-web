# For dealing with the tenancies, evictions and emigrations data of the Coolattin Estate

import pandas as pd
import json
import io

class TownlandData:
    def __init__(self, tenancies_path, evictions_path, emigrations_path, json_path):
        self.tenancies = pd.read_csv(tenancies_path, on_bad_lines="skip")
        self.evictions = pd.read_csv(evictions_path, on_bad_lines="skip")
        self.emigrations = pd.read_csv(emigrations_path, on_bad_lines="skip")
        self.official_list = pd.read_csv("static/data/official-aligned.csv")

        print(self.evictions.columns)

        # Setup pandas options for printing
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.expand_frame_repr", False)

        with open(json_path, encoding="utf-8") as f:
            self.geojson = json.load(f)
            for feature in self.geojson["features"]:
                name_english = feature["properties"]["TL_ENGLISH"]
                link = f'<a href="/townlands/{name_english.title()}" target="_blank">More details</a>'
                feature["properties"]["TL_URL"] = link

    def get_tenancies(self, townland):
        tenancies_data = self.tenancies[self.tenancies["townland"].str.strip().str.lower() == townland.lower()]

        if tenancies_data is None:
            return []

        return tenancies_data.reset_index(drop=True).to_dict(orient="records")

    def extract_tenancies(self, townland):
        extracted_records = self.tenancies[self.tenancies["townland1"].str.strip().str.lower() == townland.strip().lower()]
        output = io.StringIO()
        extracted_records.to_csv(output, index=False)
        return io.BytesIO(output.getvalue().encode())


    def get_evictions(self, townland):
        evictions_data = self.evictions[self.evictions["townland1"].str.lower() == townland.lower()]

        if evictions_data is None or townland.lower() == "Ballynultagh".lower():
            print(f"NO EVICTIONS -> {townland}")
            return []

        return evictions_data.reset_index(drop=True).to_dict(orient="records")

    def get_emigrations(self, townland):
        emigrations_data = self.emigrations[self.emigrations["townland1"].str.lower() == townland.lower()]

        if emigrations_data is None:
            print(f"NO EMIGRATIONS -> {townland}")
            return []

        return emigrations_data.reset_index(drop=True).to_dict(orient="records")

    def print_tenancies(self, townland):
        tenancies = self.get_tenancies(townland)
        print(tenancies)

    def print_evictions(self, townland):
        evictions = self.get_evictions(townland)
        print(evictions)

    def print_emigrations(self, townland):
        emigrations = self.get_emigrations(townland)
        print(emigrations)

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

    def get_vrti_link(self, townland):
        for index, row in self.official_list.iterrows():
            if row.iloc[0] == townland:
                return row.iloc[1]
        return None