from flask import Flask, render_template, request
import location
import max_dwelling_units
import road_setback
import max_gfa
import get_gen_images

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', development_restrictions={})

@app.route('/submit', methods=['POST'])
def submit():
    postal_code = request.form['postal_code'] #hardcoded for address(eg, only accepts 'simei green')
    boundary_coordinates = request.form['boundary_coordinates']
    target_gpr = request.form['target_gpr']

    address = postal_code or boundary_coordinates
    gpr = float(target_gpr)

    osm_id, center_coordinates, location_coordinates, geojson = location.main(address)
    
    site_area = get_gen_images.main(geojson, center_coordinates, gpr)

    maximum_gfa = max_gfa.max_gfa_excluding_rrdr(gpr, site_area)
    roads_setback = road_setback.main(location_coordinates)
    maximum_dwelling_units = max_dwelling_units.max_dwelling_units(gpr, site_area, center_coordinates)

    development_restrictions = {
        "max_gfa": maximum_gfa,
        "roads_setback": roads_setback,
        "max_dwelling_units": maximum_dwelling_units,
        "address": address,
        "gpr": gpr,
        "area": site_area
    }

    # Render the same index.html but now with the development_restrictions variable passed to it.
    return render_template('index.html', development_restrictions=development_restrictions)

if __name__ == '__main__':
    app.run(debug=True)