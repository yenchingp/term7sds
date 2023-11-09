import requests
import json
import re
import csv

def get_osm_id(address):
    print(address)
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

def main(address):
    osm_id, center_coordinates = get_osm_id(address)
    if osm_id is None:
        return
    location = get_coordinates_of_way(osm_id)
    geojson = coordinates_to_geojson(location)
    return osm_id, center_coordinates, location, geojson

address = 'simei green'
_, center_coord, _, geojson = main(address)
print(center_coord)
print(geojson)

geojson_feature = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Polygon",
        "coordinates": [geojson]
    }
}
geojson_str = json.dumps(geojson_feature)
encoded_geojson = requests.utils.quote(geojson_str)


# Replace the placeholder values with your actual data
access_token = ''  # Replace with your Mapbox access token
lon, lat = center_coord  # Replace with the center longitude and latitude of your GeoJSON
zoom = 17  # Set the zoom level as needed
width, height = 1280, 720  # Set the desired image dimensions
style_id = 'clogxdq2i007r01qr5gmsc907'

# Construct the API request URL
maskurl = f"https://api.mapbox.com/styles/v1/zyjy118/{style_id}/static/geojson({encoded_geojson})/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
#maskurl = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/geojson({encoded_geojson})/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
# Send the GET request
#response1 = requests.get(url)
response2 = requests.get(maskurl)

# if response1.status_code == 200:
#     # Save the image to a file
#     with open('site.png', 'wb') as image_file:
#         image_file.write(response1.content)
#     print('Image saved successfully!')
# else:
#     print(f"Failed to retrieve the image: {response1.status_code} - {response1.content}")

if response2.status_code == 200:
    # Save the image to a file
    with open('site_masked.png', 'wb') as image_file:
        image_file.write(response2.content)
    print('Masked Image saved successfully!')
else:
    print(f"Failed to retrieve the masked image: {response2.status_code} - {response2.content}")