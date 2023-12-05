import requests
import location
import max_dwelling_units
import road_setback
import max_gfa
import get_gen_images

address = "1 Canberra Singapore"  # Format: postal code,  country
gpr = 2.5
# expected du=561(/85), roadsetback: ['', 'CAT3', 'Building â‰¤ 5 storeys\n7.5m (3m)Building â‰¥ 6 storeys\n10m (3m)']

osm_id, center_coordinates, location, geojson = location.main(address)
site_pixels = get_gen_images.main(geojson, center_coordinates, gpr)
site_area = site_pixels * 1.3335
print(f"{address} \nTarget GPR: {gpr}, Site area: {site_area} msq")
max_gfa = max_gfa.max_gfa_excluding_rrdr(gpr, site_area)
print(max_gfa)
roads_setback = road_setback.main(location)
max_dwelling_units = max_dwelling_units.max_dwelling_units(gpr, site_area, center_coordinates)
