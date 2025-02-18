# For dealing with population data
import pandas as pd

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

    def get_townland_pops_male(self, townland):
        td = self.get_townland_data(townland)

        if td is None:
            return None

        pop_data = {
            1841: int(td["1841 Male"][0]),
            1851: int(td["1851 Male"][0]),
            1861: int(td["1861 Male"][0]),
            1871: int(td["1871 Male"][0]),
            1881: int(td["1881 Male"][0]),
            1891: int(td["1891 Male"][0]),
        }

        return pop_data

    def get_townland_pops_female(self, townland):
        td = self.get_townland_data(townland)

        if td is None:
            return None

        pop_data = {
            1841: int(td["1841 Female"][0]),
            1851: int(td["1851 Female"][0]),
            1861: int(td["1861 Female"][0]),
            1871: int(td["1871 Female"][0]),
            1881: int(td["1881 Female"][0]),
            1891: int(td["1891 Female"][0]),
        }

        return pop_data

    def get_townland_pops_combined(self, townland):
        td = self.get_townland_data(townland)

        if td is None:
            return None

        pop_data = {
            1841: int(td["1841 Male"][0]) + int(td["1841 Female"][0]),
            1851: int(td["1851 Male"][0]) + int(td["1851 Female"][0]),
            1861: int(td["1861 Male"][0]) + int(td["1861 Female"][0]),
            1871: int(td["1871 Male"][0] + int(td["1871 Female"][0])),
            1881: int(td["1881 Male"][0] + int(td["1881 Female"][0])),
            1891: int(td["1891 Male"][0] + int(td["1891 Female"][0])),
        }

        return pop_data

if __name__ == '__main__':
    census_test = CensusData("static/data/wicklow-census-data.csv")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    td = census_test.get_townland_data("Askintinny")
    print(census_test.get_townland_pops_male("Toberpatrick"))