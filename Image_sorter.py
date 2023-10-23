import os
import cv2
import numpy as np

# Define the input folder path containing the images
input_folder = "Compiled_OSM_screenshots - Copy\Input" 

# Define the output folders for the three categories
output_folder_small = "blue_small"  # Folder for images with a small amount of blue pixels
output_folder_medium = "blue_medium"  # Folder for images with a medium amount of blue pixels
output_folder_large = "blue_large"  # Folder for images with a large amount of blue pixels

# Create the output folders if they don't exist
os.makedirs(output_folder_small, exist_ok=True)
os.makedirs(output_folder_medium, exist_ok=True)
os.makedirs(output_folder_large, exist_ok=True)

# Thresholds for categorizing images
blue_pixel_threshold_small = 0.04  # Images with less than 5% blue pixels
blue_pixel_threshold_medium = 0.1  # Images with 5-10% blue pixels

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)

        # Load the image
        image = cv2.imread(image_path)

        if image is not None:
            try:
                # Convert the image to the HSV color space
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # Define the lower and upper bounds for blue in HSV
                lower_blue = np.array([100, 50, 50])
                upper_blue = np.array([130, 255, 255])

                # Create a binary mask for blue color in the HSV image
                blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

                # Count the number of blue pixels
                blue_pixels = np.count_nonzero(blue_mask)

                # Calculate the percentage of blue pixels
                total_pixels = image.shape[0] * image.shape[1]
                blue_pixel_percentage = blue_pixels / total_pixels

                # Categorize the image based on the blue pixel percentage
                if blue_pixel_percentage < blue_pixel_threshold_small:
                    output_path = os.path.join(output_folder_small, filename)
                elif blue_pixel_threshold_small <= blue_pixel_percentage < blue_pixel_threshold_medium:
                    output_path = os.path.join(output_folder_medium, filename)
                else:
                    output_path = os.path.join(output_folder_large, filename)

                # Move the image to the appropriate category folder
                os.rename(image_path, output_path)
                
                print(f"Processed: {filename}, Blue Percentage: {blue_pixel_percentage * 100:.2f}%")

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
        else:
            print(f"Failed to load: {filename}")

print("Images sorted into categories based on blue pixel percentage.")
