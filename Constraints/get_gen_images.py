import json
import requests
import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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
            "fill-opacity": "1.0",
            "stroke-width" : 0,
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [geojson]
        }
    }
    geojson_str = json.dumps(geojson_feature)
    encoded_geojson = requests.utils.quote(geojson_str)
    return encoded_geojson

def og_geojson_maker(geojson):
    geojson_feature = {
        "type": "Feature",
        "properties": {
            "fill": "#E6E4E0",
            "fill-opacity": "1.0", 
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
    encoded_geojson_buildings = rd_geojson_maker(geojson, 1.4) # mask is always green
    encoded_geojson_og = og_geojson_maker(geojson)
    # call mapbox api
    access_token = 'sk.eyJ1IjoieWVuY2hpbmdwIiwiYSI6ImNsb3FrZ2U1czBqZjkycWx3cXVlbDRzOXkifQ.hTjiIfuNE7I-KhYqJfQkFw'  # Replace with your Mapbox access token
    lon, lat = center_coordinates  # Replace with the center longitude and latitude of your GeoJSON
    zoom = 16 # Set the zoom level as needed
    width, height = 512,512  # Set the desired image dimensions
    style_id = 'clogyeist005901nzfv9veyfa'
    mask_rd_url = f"https://api.mapbox.com/styles/v1/zyjy118/{style_id}/static/geojson({encoded_geojson_rd})/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
    mask_buildings_url =  f"https://api.mapbox.com/styles/v1/zyjy118/{style_id}/static/geojson({encoded_geojson_buildings})/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
    ogurl = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/geojson({encoded_geojson_og})/{lon},{lat},{zoom}/{width}x{height}@2x?access_token={access_token}"
    response1 = requests.get(ogurl)
    response2 = requests.get(mask_rd_url)
    response3 = requests.get(mask_buildings_url)
    print(response1.status_code, response2.status_code, response3.status_code)
    if response1.status_code == 200:
        # Save the image to a file
        with open('./site.png', 'wb') as image_file:
            image_file.write(response1.content)
        print('Og Image saved successfully!')
    else:
        print(f"Failed to retrieve the image: {response1.status_code} - {response1.content}")
    
    if response2.status_code == 200:
        # Save the image to a file
        with open('./rd_input.png', 'wb') as image_file:
            image_file.write(response2.content)
        print('Masked Image Rd saved successfully!')
    else:
        print(f"Failed to retrieve the masked image: {response2.status_code} - {response2.content}")
    
    if response3.status_code == 200:
        # Save the image to a file
        with open('./site_masked_buildings.png', 'wb') as image_file:
            image_file.write(response3.content)
        print('Masked Image Buildings saved successfully!')
    else:
        print(f"Failed to retrieve the masked image: {response2.status_code} - {response2.content}")

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

def rgb_colour(gpr):
    building_rgb = []
    rd_rgb = []
    if gpr >= 1.4 and gpr < 1.6:
        building_rgb = [255, 10, 169]
        rd_rgb = [0,255,0]
    elif gpr >= 1.6 and gpr < 2.1:
        building_rgb = [200,130,60]
        rd_rgb = [200,130,60]
    elif gpr >= 2.1 and gpr < 2.8:
        building_rgb = [0,0,255]
        rd_rgb = [0,0,0]
    elif gpr >= 2.8 and gpr < 3.0:
        building_rgb = [255,0,0]
        rd_rgb = [255,0,0]
    elif gpr >= 3.0:
        building_rgb = [0,0,0]
        rd_rgb = [0,0,255]
    return rd_rgb, building_rgb

def apply_to_og_site():
    return

def create_binary_mask(arr, target_color, threshold=30):
    lower_bound = np.array(target_color) - threshold
    upper_bound = np.array(target_color) + threshold
    mask = (arr[:, :, :3] >= lower_bound) & (arr[:, :, :3] <= upper_bound)
    return np.all(mask, axis=-1)

def extract_building_regions(arr, target_color, threshold=30):
    lower_bound = np.array(target_color) - threshold
    upper_bound = np.array(target_color) + threshold
    mask = (arr[:, :, :3] >= lower_bound) & (arr[:, :, :3] <= upper_bound)
    return np.all(mask, axis=-1)

def approx_contours(contours, epsilon_factor=0.02):
    approximated_contours = []
    for contour in contours:
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        approximated_contours.append(approx)
    return approximated_contours

def remove_nested_rectangles(rectangles):
    non_nested = []
    for rect in rectangles:
        x1, y1, w1, h1 = rect
        nested = False
        for other_rect in rectangles:
            if other_rect == rect:
                continue
            x2, y2, w2, h2 = other_rect
            if x1 >= x2 and y1 >= y2 and x1 + w1 <= x2 + w2 and y1 + h1 <= y2 + h2:
                nested = True
                break
        if not nested:
            non_nested.append(rect)
    return non_nested

def merge_rectangles(rectangles, distance_threshold):
    merged = []
    while rectangles:
        a = rectangles.pop(0)
        to_merge = [a]
        i = 0
        while i < len(rectangles):
            b = rectangles[i]
            if is_close(a, b, distance_threshold):
                to_merge.append(b)
                rectangles.pop(i)
            else:
                i += 1
        xs = [x for x, _, w, _ in to_merge for x in [x, x+w]]
        ys = [y for _, y, _, h in to_merge for y in [y, y+h]]
        merged.append((min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)))
    return merged

def is_close(rect1, rect2, threshold):
    """
    Check if two rectangles are close to each other based on a threshold.
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    center1 = (x1 + w1 / 2, y1 + h1 / 2)
    center2 = (x2 + w2 / 2, y2 + h2 / 2)
    distance = np.hypot(center1[0] - center2[0], center1[1] - center2[1])
    return distance < threshold

def smooth_contours(contours, alpha=0.02):
    # alpha parameter controls the approximation accuracy
    smoothed_contours = [cv2.approxPolyDP(cnt, alpha * cv2.arcLength(cnt, True), True) for cnt in contours]
    return smoothed_contours

def extract_raw_buildings(mask_rgb, building_rgb, mask_path, gen_model_path, model_name):
    og_path = "site.png"
    mask_path = mask_path
    gen_model_path = gen_model_path
    model = model_name

    og_image = Image.open(og_path).convert('RGB')
    masked_image = Image.open(mask_path).convert('RGB')
    gen_image = Image.open(gen_model_path).convert('RGB')

    og_image = og_image.resize((512, 512))
    masked_image = masked_image.resize((512, 512))

    og_array = np.array(og_image)
    masked_image_array = np.array(masked_image)
    gen_image_array = np.array(gen_image)
    
    #extract buildings
    site_mask = create_binary_mask(masked_image_array, mask_rgb)
    mask_pixels = np.sum(site_mask)
    gen_image_array[~site_mask] = [255,255,255]
    gen_building_mask = extract_building_regions(gen_image_array, building_rgb) # for rd its always pink buildings
    # put raw buildings onto og site
    colored_paper = np.full((og_array.shape[0], og_array.shape[1], 3), [230, 228, 224], dtype=np.uint8) #light brown site
    colored_paper[gen_building_mask] = [220,217,214] #dark brown buildings
    og_array[site_mask] = colored_paper[site_mask]
    raw_gen = Image.fromarray(og_array)
    raw_gen.save(f"static\\raw_{model}.png")

    # get contours
    building_mask = gen_building_mask.copy()
    building_mask = (building_mask * 255).astype(np.uint8)
    blurred = cv2.GaussianBlur(building_mask, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    approximated_contours = approx_contours(contours)
    blank_image_for_contour = np.zeros_like(building_mask)
    approximated_contours_image = cv2.drawContours(blank_image_for_contour, approximated_contours, -1, (255), 5)

    #get rectangles
    colored_paper2 = np.full((og_array.shape[0], og_array.shape[1], 3), [230, 228, 224], dtype=np.uint8) #light brown site
    rectangle_color = (220,217,214)
    rectangles = [cv2.boundingRect(contour) for contour in approximated_contours]
    non_nested_rectangles = remove_nested_rectangles(rectangles)
    distance_threshold = 10
    merged_rectangles = merge_rectangles(non_nested_rectangles, distance_threshold)
    min_width = 10
    min_height = 10
    for x, y, w, h in merged_rectangles:
        if w >= min_width and h >= min_height:
            cv2.rectangle(colored_paper2, (x, y), (x + w, y + h), rectangle_color, -1)
    og_array[site_mask] = colored_paper2[site_mask]
    rec_gen = Image.fromarray(og_array)
    rec_gen.save(f"static\\rec_{model}.png")

    # smooth
    colored_paper3 = np.full((og_array.shape[0], og_array.shape[1], 3), [230, 228, 224], dtype=np.uint8)
    contour_colour = (220,217,214)
    kernel = np.ones((3,3), np.uint8)
    opened_image = cv2.morphologyEx(approximated_contours_image, cv2.MORPH_OPEN, kernel, iterations=1)
    closed_image = cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, kernel, iterations=1)
    contours, _ = cv2.findContours(closed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_pixels = sum(cv2.contourArea(contour) for contour in contours)
    min_area_threshold = 0.15*contour_pixels
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold] #discard small contours
    smoothed_contours = smooth_contours(large_contours)
    cv2.drawContours(colored_paper3, smoothed_contours, -1, contour_colour, thickness=cv2.FILLED)
    og_array[site_mask] = colored_paper3[site_mask]
    smooth_gen = Image.fromarray(og_array)
    smooth_gen.save(f"static\\smooth_{model}.png")
    return mask_pixels


def main(geojson, center_coordinates, gpr):
    get_mapbox_image(geojson, center_coordinates, gpr)
    prep_buildings_model_input(gpr, "site_masked_buildings.png", "buildings_input.png")
    get_gen_image("rd_input.png", "buildings_input.png")
    rd_mask_rgb ,  buildings_building_rgb = rgb_colour(gpr)
    extract_raw_buildings(rd_mask_rgb, [255,10,169], "rd_input.png", "gen_rd1.png", "rd1")
    mask_pixels = extract_raw_buildings([0,255,0], buildings_building_rgb, "buildings_input.png", "gen_b2.png", "b2")
    extract_raw_buildings([0,255,0], buildings_building_rgb, "buildings_input.png", "gen_b3.png", "b3")
    site_area = mask_pixels*1.3335
    return site_area