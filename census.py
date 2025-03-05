# For dealing with population data
import json

import pandas as pd
import plotly.graph_objs as go
import plotly


class CensusData:
    def __init__(self, census_path):
        self.data = pd.read_csv(census_path)

    # Finds the townlands population data and returns it as a dictionary
    def get_townland_data(self, townland):
        townland_data = self.data[self.data["Townland"].str.lower() == townland.lower()]

        if townland_data is None:
            return None

        print(townland_data)
        return townland_data.reset_index(drop=True).to_dict()

    # Gets population of males in a townland and returns as a dictionary
    def get_townland_pops_male(self, townland):
        td = self.get_townland_data(townland)

        if td is None:
            return None

        pop_data = {
            1841: float(td["1841 Male"][0]),
            1851: float(td["1851 Male"][0]),
            1861: float(td["1861 Male"][0]),
            1871: float(td["1871 Male"][0]),
            1881: float(td["1881 Male"][0]),
            1891: float(td["1891 Male"][0]),
        }

        return pop_data

    # Gets population of females in townland and returns as a dictionary
    def get_townland_pops_female(self, townland):
        td = self.get_townland_data(townland)

        if td is None:
            return None

        pop_data = {
            1841: float(td["1841 Female"][0]),
            1851: float(td["1851 Female"][0]),
            1861: float(td["1861 Female"][0]),
            1871: float(td["1871 Female"][0]),
            1881: float(td["1881 Female"][0]),
            1891: float(td["1891 Female"][0]),
        }

        return pop_data

    # Combines male and female population for townland and returns as dictionary
    def get_townland_pops_combined(self, townland):
        td = self.get_townland_data(townland)

        if td is None:
            return None

        pop_data = {
            1841: float(td["1841 Male"][0]) + float(td["1841 Female"][0]),
            1851: float(td["1851 Male"][0]) + float(td["1851 Female"][0]),
            1861: float(td["1861 Male"][0]) + float(td["1861 Female"][0]),
            1871: float(td["1871 Male"][0] + float(td["1871 Female"][0])),
            1881: float(td["1881 Male"][0] + float(td["1881 Female"][0])),
            1891: float(td["1891 Male"][0] + float(td["1891 Female"][0])),
        }

        return pop_data

    # Generates combined population chart of townland for years 1841-1891
    def generate_population_chart(self, townland):
        data = self.get_townland_pops_combined(townland)
        years = list(data.keys())
        populations = list(data.values())
        fig = go.Figure(data=[go.Bar(x=years, y=populations, marker=dict(color="yellow"))])
        fig.update_layout(title=f"Population of {townland} over time", xaxis_title="Year", yaxis_title="Population")
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        print(f"=============== Graph for {townland} generated successfully =============")
        return graph_json

# Local testing methods
if __name__ == '__main__':
    census_test = CensusData("static/data/wicklow-census-data.csv")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    td = census_test.get_townland_data("Askintinny")
    print(census_test.get_townland_pops_male("Toberpatrick"))
