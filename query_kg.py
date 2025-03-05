# Provided by Alex Randles, ADAPT Centre, 11/02/2024
from SPARQLWrapper import SPARQLWrapper, JSON
import json


# SPARQL query to search for townlands containing the given place name
def create_place_name_query(place_name):
    sparql_query = f"""
    PREFIX crm: <http://erlangen-crm.org/current/>
    PREFIX vrti: <https://ont.virtualtreasury.ie/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT *
    WHERE {{

        GRAPH <http://localhost:8890/presentday> {{
            ?Townland rdfs:label ?TownlandName;
                   crm:P2_has_type vrti:PresentDayTownland .

            # Filter for English language labels and match place name case-insensitively
            FILTER(langMatches(lang(?TownlandName), "en"))
            FILTER(CONTAINS(LCASE(?TownlandName), LCASE("{place_name}")))

        }}
    }}

    # Order by shortest match 
    ORDER BY ASC(STRLEN(?TownlandName))
    """

    return sparql_query


# Function to query a SPARQL endpoint for a given place name
def query_vrti_endpoint(sparql_query):
    endpoint_url = "https://vrti-graph-explorer.adaptcentre.ie/sparql/"

    # Initialize SPARQLWrapper with the endpoint URL
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)  # Set return format to JSON

    try:
        # Execute query and return results
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        print(f"Error executing SPARQL query: {e}")
        return None


def main():
    place_name = "Tinahely"  # Set place name to search for
    sparql_query = create_place_name_query(place_name)
    query_results = query_vrti_endpoint(sparql_query)

    print(query_results)
    if query_results:
        # Print each ?Townland ?TownlandName result from the query
        for result in query_results:
            print(result.get("Townland", {}).get("value"))
            print(result.get("TownlandName", {}).get("value"))
    else:
        print("No results found.")


if __name__ == "__main__":
    main()
