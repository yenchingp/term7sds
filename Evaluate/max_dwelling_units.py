from shapely.geometry import Polygon, Point
import json

def max_dwelling_units(gpr, site_area, center_coordinate):

    latitude, longitude = center_coordinate
    map1 = False
    map2 = False

    # Coordinates of regions in Map 1(central area)
    json_file_path = "Map1.json"
    with open(json_file_path, "r") as json_file:
        map1_coordinates_data = json.load(json_file)
    # Loop through each set of Map 1 coordinates and check if the point is within the polygon
    for key, coordinates_list in map1_coordinates_data.items():
        polygon = Polygon(coordinates_list)
        point = Point(latitude, longitude)
        if polygon.contains(point):
            map1 = True
            break  # If it's inside one of the polygons, break the loop

    # Coordinates of regions in Map 2
    json_file_path = "Map2.json"
    with open(json_file_path, "r") as json_file:
        map2_coordinates_data = json.load(json_file)
    # Loop through each set of Map 2 coordinates and check if the point is within the polygon
    for key, coordinates_list in map2_coordinates_data.items():
        polygon = Polygon(coordinates_list)
        point = Point(latitude, longitude)
        if polygon.contains(point):
            map2 = True
            break  # If it's inside one of the polygons, break the loop

    # if not in map 2 and not in central area
    max_du = 0
    if (map2 is False) and (map1 is False):
        max_du = (gpr * site_area) / 85
        print(f"Location is not in Map 2. Max dwelling unit is {max_du}.")

    # if not in central area but in map 2
    if map2 is True:
        max_du = (gpr * site_area) / 100
        print(f"Location is in Map 2. Max dwelling unit is {max_du}.")

    # if in city
    if map1 is True:
        print(f"Location is in central area. Refer to URA for Max dwelling units.")

    return
