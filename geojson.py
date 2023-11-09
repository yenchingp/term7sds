import requests

def get_osm_id(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            center_coordinate = float(data[0].get("lon")), float(data[0].get("lat"))
            osm_id = data[0]['osm_id']
            return osm_id, center_coordinate
        else:
            print("No results found for the address.")
            return None
    else:
        print("Error:", response.status_code)
        return None

def get_coordinates_of_way(osm_id):
    overpass_url = "http://overpass-api.de/api/interpreter"
    way_query = f"""
    [out:json];
    way({osm_id});
    out geom;
    """

    try:
        response = requests.get(overpass_url, params={'data': way_query})
        response.raise_for_status()
        way_data = response.json()
        if not way_data['elements']:
            print(f"Way {osm_id} not found!")
            return []

        coords = way_data['elements'][0]['geometry']
        return [(point['lat'], point['lon']) for point in coords]

    except requests.RequestException as e:
        print(f"Error fetching data for way {osm_id} from Overpass API: {e}")
        return []


def coordinates_to_geojson(coordinates, osm_type='way'):
    if not coordinates or coordinates[0] != coordinates[-1]:
        print("The provided coordinates do not form a closed loop. Cannot create a Polygon.")
        return None

    # Flip the coordinates from (lat, lon) to (lon, lat)
    flipped_coordinates = [[lon, lat] for lat, lon in coordinates]
    
    return flipped_coordinates

address = 'simei green'
def main(address):
    osm_id, center_coordinates = get_osm_id(address)
    location = get_coordinates_of_way(osm_id)
    geojson = coordinates_to_geojson(location)
    return osm_id, center_coordinates, location, geojson

_, center_coordinates, ___, geojson = main(address)
print(center_coordinates)
print(geojson)