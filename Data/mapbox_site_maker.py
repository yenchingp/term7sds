import requests
import re
import csv

addresses = []
index_names = []
csv_file_path = 'condo_data_new_v5.csv'

# Open the CSV file and read its contents
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Iterate through each row and extract the value from the first column
    for row in csv_reader:
        if row:  # Check if the row is not empty
            zero_column_value = row[0] # Index 0 corresponds to the first column
            first_column_value = row[2]  
            index_names.append(zero_column_value)
            addresses.append(first_column_value)
addresses.pop(0)
index_names.pop(0)
# row filter
filter = 5
addresses = addresses[filter:]
index_names = index_names[filter:]

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
            center_coordinate = [float(data[0].get("lon")), float(data[0].get("lat"))]
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

def template_editor(name, poly, centre):
    # Define the HTML file name
    html_file = "mapbox_template.html"
    if poly == None:
        new_html_file = "mapbox_rd/mapbox_gt/" + name + "_gt.html"
    else:
        new_html_file = "mapbox_rd/mapbox_input/" + name + "_input.html"

    # Define the variables you want to modify
    variable1_name = 'polygon_coordinate'
    new_value1_tuple = poly
    new_value1 = str(new_value1_tuple)

    variable2_name = 'center_coordinate'
    new_value2_tuple = centre
    new_value2 = str(new_value2_tuple)

    # Read the HTML file
    with open(html_file, "r") as file:
        html_content = file.read()

    html_content = html_content.replace('polygon_coordinate', new_value1)
    html_content = html_content.replace('center_coordinate', new_value2)

    # Write the updated HTML content back to the file
    with open(new_html_file, "w") as file:
        file.write(html_content)

    print("Variable '{}' updated to '{}' and variable '{}' updated to '{}' in '{}'.".format(variable1_name, new_value1, variable2_name, new_value2, html_file))


for index_name, address in zip(index_names, addresses):
    _, center_coordinates, ___, geojson = main(address)
    # print(center_coordinates)
    # print(geojson)

    template_editor(index_name, geojson, center_coordinates)
    template_editor(index_name, None, center_coordinates)

print('Scraping complete!')