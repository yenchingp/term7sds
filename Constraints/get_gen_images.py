import json
import requests
import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def rd_geojson_maker(geojson, gpr):
    rgb = ""
    if gpr >= 1.4 and gpr < 1.6:
        rgb = "#00FF00"
    elif gpr >= 1.6 and gpr < 2.1:
        rgb = "#C8823C"
    elif gpr >= 2.1 and gpr < 2.8:
        rgb = "#000000"
    elif gpr >= 2.8 and gpr < 3.0:
        rgb = "#FF0000"
    elif gpr >= 3.0:
        rgb = "#0000FF"
    geojson_feature = {
        "type": "Feature",
        "properties": {
            "fill": rgb,
            "fill-opacity": "1.0"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [geojson]
        }
    }
    geojson_str = json.dumps(geojson_feature)
    encoded_geojson = requests.utils.quote(geojson_str)
    return encoded_geojson

def buildings_geojson_maker(geojson):
    geojson_feature = {
        "type": "Feature",
        "properties": {
            "fill": "#00FF00",
            "fill-opacity": "1.0"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [geojson]
        }
    }
    geojson_str = json.dumps(geojson_feature)
    encoded_geojson = requests.utils.quote(geojson_str)
    return encoded_geojson

def get_mapbox_image(geojson,center_coordinates, gpr):
    encoded_geojson_rd = rd_geojson_maker(geojson, gpr)
    encoded_geojson_buildings = buildings_geojson_maker(geojson) # mask is always green
    # call mapbox api
    access_token = 'sk.eyJ1IjoieWVuY2hpbmdwIiwiYSI6ImNsb3FrZ2U1czBqZjkycWx3cXVlbDRzOXkifQ.hTjiIfuNE7I-KhYqJfQkFw'  # Replace with your Mapbox access token
    lon, lat = center_coordinates  # Replace with the center longitude and latitude of your GeoJSON
    zoom = 16 # Set the zoom level as needed
    width, height = 512,512  # Set the desired image dimensions
    style_id = 'clogyeist005901nzfv9veyfa'
    mask_rd_url = f"https://api.mapbox.com/styles/v1/zyjy118/{style_id}/static/geojson({encoded_geojson_rd})/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
    mask_buildings_url =  f"https://api.mapbox.com/styles/v1/zyjy118/{style_id}/static/geojson({encoded_geojson_buildings})/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
    ogurl = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
    response1 = requests.get(ogurl)
    response2 = requests.get(mask_rd_url)
    response3 = requests.get(mask_buildings_url)
    if response1.status_code == 200:
        # Save the image to a file
        with open('site.png', 'wb') as image_file:
            image_file.write(response1.content)
        print('Og Image saved successfully!')
    else:
        print(f"Failed to retrieve the image: {response1.status_code} - {response1.content}")
    if response2.status_code == 200:
        # Save the image to a file
        with open('rd_input.png', 'wb') as image_file:
            image_file.write(response2.content)
        print('Masked Image Rd saved successfully!')
    else:
        print(f"Failed to retrieve the masked image: {response2.status_code} - {response2.content}")
    if response3.status_code == 200:
        # Save the image to a file
        with open('site_masked_buildings.png', 'wb') as image_file:
            image_file.write(response3.content)
        print('Masked Image Buildings saved successfully!')
    else:
        print(f"Failed to retrieve the masked image: {response2.status_code} - {response2.content}")
    return

def prep_buildings_model_input(gpr, input_image, output_image): #BGR
    image = cv2.imread(input_image)
    lower_pink = (160, 0, 245) 
    upper_pink = (200, 100, 255)
    pink_mask = cv2.inRange(image, lower_pink, upper_pink)
    if gpr >= 1.4 and gpr < 1.6:
        image = image
    elif gpr >= 1.6 and gpr < 2.1:
        image[pink_mask > 0] = [60,130,200]
    elif gpr >= 2.1 and gpr < 2.8:
        image[pink_mask > 0] = [255, 0, 0]
    elif gpr >= 2.8 and gpr < 3.0:
        image[pink_mask > 0] = [0, 0, 255]
    elif gpr >= 3.0:
        image[pink_mask > 0] = [0, 0, 0]
    cv2.imwrite(output_image, image)
    return

def get_gen_image(rd_input_image, buildings_input_image):
    rd_image = tf.io.read_file(rd_input_image)
    rd_image = tf.io.decode_png(rd_image)
    rd_image = tf.cast(rd_image, tf.float32)
    rd_image = tf.image.resize(rd_image, [512, 512], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    rd_image = tf.expand_dims(rd_image, axis=0)
    rd_image = (rd_image / 127.5) - 1
    rd1_model = tf.keras.models.load_model('..\\Model\\rd\\generatorv5_final_rd_1.h5')
    gen_rd1 = rd1_model(rd_image, training=True)
    gen_rd1 = gen_rd1[0]
    gen_rd1 = (gen_rd1 + 1) / 2
    gen_rd1 = tf.clip_by_value(gen_rd1, 0, 1)

    buildings_image = tf.io.read_file(buildings_input_image)
    buildings_image = tf.io.decode_png(buildings_image)
    buildings_image = tf.cast(buildings_image, tf.float32)
    buildings_image = tf.image.resize(buildings_image, [512, 512], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    buildings_image = tf.expand_dims(buildings_image, axis=0)
    buildings_image = (buildings_image / 127.5) - 1
    b2_model = tf.keras.models.load_model('..\\Model\\buildings\\generatorv5_final_buildings_2.h5')
    gen_b2 = b2_model(buildings_image, training=True)
    gen_b2 = gen_b2[0]
    gen_b2 = (gen_b2 + 1) / 2
    gen_b2 = tf.clip_by_value(gen_b2, 0, 1)

    b3_model = tf.keras.models.load_model('..\\Model\\buildings\\generatorv5_final_buildings_3.h5')
    gen_b3 = b3_model(buildings_image, training=True)
    gen_b3 = gen_b3[0]
    gen_b3 = (gen_b3 + 1) / 2
    gen_b3 = tf.clip_by_value(gen_b3, 0, 1)
 
    plt.imsave("gen_rd1.png", gen_rd1.numpy())
    plt.imsave("gen_b2.png", gen_b2.numpy())
    plt.imsave("gen_b3.png", gen_b3.numpy())
    return


def main(geojson, center_coordinates, gpr):
    get_mapbox_image(geojson, center_coordinates, gpr)
    prep_buildings_model_input(gpr, "site_masked_buildings.png", "buildings_input.png")
    get_gen_image("rd_input.png", "buildings_input.png")
    return

center_coordinates = (103.78378301045407, 1.30560345)
geojson = [[103.784756, 1.3050353], [103.7847946, 1.3061424], [103.7850962, 1.3068138], [103.7840787, 1.3068373], [103.7840465, 1.3064766], [103.7830011, 1.3065207], [103.7826663, 1.3050645], [103.784756, 1.3050353]]
tar_gpr = 2.1
main(geojson, center_coordinates, tar_gpr)