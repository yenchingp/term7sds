from flask import Flask, render_template, request, jsonify, url_for
import location
import max_dwelling_units
import road_setback
import max_gfa

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
    site_area = 20800 #this hardcoded

    osm_id, center_coordinates, location_coordinates = location.main(address)
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
    image_urls = [
        url_for('static', filename='image1.jpg'),
        url_for('static', filename='image2.jpg'),
        url_for('static', filename='image3.jpg'),
        url_for('static', filename='image4.jpg'),
        url_for('static', filename='image5.jpg'),
        url_for('static', filename='image6.jpg'),
        url_for('static', filename='image7.jpg'),
        url_for('static', filename='image8.jpg'),
        url_for('static', filename='image9.jpg'),
    ]

    response_data = {
        "development_restrictions": development_restrictions,
        "image_urls": image_urls
    }
    print(f"dev restrictions: {development_restrictions}")

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
