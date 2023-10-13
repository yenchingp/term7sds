import requests
import max_dwelling_units

address = "479252, Singapore"  # Format: postal code,  country
postal_code = "479252"
country = "Singapore"
gpr = 2.5
site_area = 20800
# expected du=561(/85), roadsetback: ['', 'CAT3', 'Building â‰¤ 5 storeys\n7.5m (3m)Building â‰¥ 6 storeys\n10m (3m)']

# function to get the the osm id and the coordinates of the point location of a postal code
def get_osmid_pointlocation(postal_code, country):
    base_url = "https://nominatim.openstreetmap.org/search"
    query = f"{postal_code}, {country}"
    params = {
        "q": query,
        "format": "json",
    }
    coordinate = requests.get(base_url, params=params)
    data = coordinate.json()

    if data:
        way_id = data[0].get("place_id")
        center_coordinate = float(data[0].get("lat")), float(data[0].get("lon"))
        return way_id, center_coordinate
    return None

# get id of the points that makes the plot of the location
def get_nodes_of_way(way_id):
    base_url = f"https://api.openstreetmap.org/api/0.6/way/{way_id}.json"
    response = requests.get(base_url)
    data = response.json()
    print(data['elements'][0]['nodes'])
    return data['elements'][0]['nodes']

# get coordinates of points that makes the plot of the location
def get_node_details(node_id):
    base_url = f"https://api.openstreetmap.org/api/0.6/node/{node_id}.json"
    response = requests.get(base_url)
    return response.json()


way_id, center_coordinate = get_osmid_pointlocation(postal_code, country)

# complie the coordinates of the location. type: list of tuples
nodes = get_nodes_of_way(way_id)
location = []
for node_id in nodes:
    node_details = get_node_details(node_id)
    latitude = node_details['elements'][0]['lat']
    longitude = node_details['elements'][0]['lon']
    location.append((latitude, longitude))

print(f"{country}, {postal_code} \nTarget GPR: {gpr}, Site area: {site_area}")
max_dwelling_units.max_dwelling_units(gpr, site_area, center_coordinate)