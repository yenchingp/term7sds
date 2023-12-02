import requests
import time

def get_roads_around_location(location, distance):
    overpass_url = "http://overpass-api.de/api/interpreter"

    lat, lon = location
    road_query = f"""
    [out:json];
    way(around:{distance},{lat},{lon})['highway'~'motorway|primary|secondary|tertiary|residential|service'];
    out geom;
    """.strip()
    try:
        response = requests.get(overpass_url, params={'data': road_query})
        response.raise_for_status()
        roads_data = response.json()
        return roads_data['elements']

    except requests.RequestException as e:
        print(f"Error fetching roads around {location} from Overpass API: {e}")
        return []


def get_roads(location, distance=30):
    all_roads = []
    for coord in location:
        roads_data = get_roads_around_location(coord, distance)
        all_roads.extend(roads_data)

        # To avoid hitting rate limits or overloading the server
        time.sleep(1)

    highways_and_names = []
    for road in all_roads:
        if 'tags' in road and 'highway' in road['tags'] and 'name' in road['tags']:
            highways_and_names.append({
                'highway': road['tags']['highway'],
                'name': road['tags']['name']
            })

    # Removing duplicates from the list
    affecting_roads = []
    for item in highways_and_names:
        if item not in affecting_roads:
            affecting_roads.append(item)

    return affecting_roads

def main(location):
    roads = get_roads(location)
    output = 'Setback details: '
    for road in roads:
        if road['highway'] == 'motorway': #CAT1
            output += f"\n {road['name']}, CAT 1: If 6 storeys and above, 30m road buffer, including 5m green buffer. Otherwise, 24m road buffer, including 5m green buffer. "
        elif road['highway'] == 'trunk': #CAT2
            output += f"\n {road['name']}, CAT 2: If 6 storeys and above, 15m road buffer, including 5m green buffer. Otherwise, 12m road buffer, including 5m green buffer. "
        elif road['highway'] == 'primary'or 'secondary': #CAT3
            output += f"\n {road['name']}, CAT 3: If 6 storeys and above, 10m road buffer, including 3m green buffer. Otherwise, 7.5m road buffer, including 3m green buffer. "
        elif road['highway'] == 'tertiary' or 'residential' or 'service': #CAT4
            output += f"\n {road['name']}, CAT 4/5: 7.5m road buffer, including 3m green buffer. "
            pass
    output += "\n 7.5m road buffer applies for all other roads. "
    print(output)
    return output
