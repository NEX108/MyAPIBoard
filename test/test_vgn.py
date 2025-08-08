import requests

def suche_haltestelle(name):
    url = "https://start.vag.de/dm/api/haltestellen.json/vag"
    response = requests.get(url, params={"name": name}, timeout=10)
    response.raise_for_status()
    return response.json()

haltestellen = suche_haltestelle("Frankenstraße")
print(haltestellen)

