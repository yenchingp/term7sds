import cv2
import os

# Function to change pink pixels to red
def change_pink_to_red(input_image_path, output_image_path):
    # Load the input image
    image = cv2.imread(input_image_path)

    # Define the lower and upper bounds of the pink color in BGR format
    lower_pink = (160, 0, 245)  # Adjust these values to match the shade of pink in your images
    upper_pink = (200, 100, 255)  # Adjust these values accordingly

    # Create a mask for the pink pixels
    pink_mask = cv2.inRange(image, lower_pink, upper_pink)

    # Replace pink pixels with red (BGR format)
    image[pink_mask > 0] = [0, 0, 255]

    # Save the modified image
    # cv2.imwrite(input_image_path + "new", image)
    cv2.imwrite(output_image_path, image)

# Function to change pink pixels to purple
def change_pink_to_purple(input_image_path, output_image_path):
    # Load the input image
    image = cv2.imread(input_image_path)

    # Define the lower and upper bounds of the pink color in BGR format
    lower_pink = (160, 0, 245)  # Adjust these values to match the shade of pink in your images
    upper_pink = (200, 100, 255)  # Adjust these values accordingly

    # Create a mask for the pink pixels
    pink_mask = cv2.inRange(image, lower_pink, upper_pink)

    # Replace pink pixels with black pixels (BGR format)
    image[pink_mask > 0] = [0, 0, 0]

    # Save the modified image as input_image_path + "new"
    # cv2.imwrite(input_image_path + "new", image)
    cv2.imwrite(output_image_path, image)

# Function to change pink pixels to cyan
def change_pink_to_cyan(input_image_path, output_image_path):
    # Load the input image
    image = cv2.imread(input_image_path)

    # Define the lower and upper bounds of the pink color in BGR format
    lower_pink = (160, 0, 245)  # Adjust these values to match the shade of pink in your images
    upper_pink = (200, 100, 255)  # Adjust these values accordingly

    # Create a mask for the pink pixels
    pink_mask = cv2.inRange(image, lower_pink, upper_pink)

    # Replace pink pixels with cyan (BGR format)
    image[pink_mask > 0] = [255, 0, 0]

    # Save the modified image as input_image_path + "new"
    # cv2.imwrite(input_image_path + "new", image)
    cv2.imwrite(output_image_path, image)

# Function to change pink pixels to brown
def change_pink_to_brown(input_image_path, output_image_path):
    # Load the input image
    image = cv2.imread(input_image_path)

    # Define the lower and upper bounds of the pink color in BGR format
    lower_pink = (160, 0, 245)  # Adjust these values to match the shade of pink in your images
    upper_pink = (200, 100, 255)  # Adjust these values accordingly

    # Create a mask for the pink pixels
    pink_mask = cv2.inRange(image, lower_pink, upper_pink)

    # Replace pink pixels with brown (BGR format)
    image[pink_mask > 0] = [60, 130, 200]

    # Save the modified image as input_image_path + "new"
    # cv2.imwrite(input_image_path + "new", image)
    cv2.imwrite(output_image_path, image)

# Function to keep pink pixels
def keep_pink(input_image_path, output_image_path):
    # Load the input image
    image = cv2.imread(input_image_path)
    cv2.imwrite(output_image_path, image)

# Function to change green pixels in mask
def change_mask_colour(input_image_path, output_image_path, gpr):
    # Load the input image
    image = cv2.imread(input_image_path)

    # Define the lower and upper bounds of the green color in BGR format
    lower_pink = (0, 255, 255)  # Adjust these values to match the shade of pink in your images
    upper_pink = (0, 255, 255)  # Adjust these values accordingly

    # Create a mask for the pink pixels
    pink_mask = cv2.inRange(image, lower_pink, upper_pink)

    if gpr == '1.6':
        # Replace pink pixels with brown (BGR format)
        image[pink_mask > 0] = [0, 255, 0]
        print("pixels changed to yellow")
    elif gpr == '2.1':
        # Replace pink pixels with cyan (BGR format)
        image[pink_mask > 0] = [0, 255, 0]
        print("pixels changed to cyan")
    elif gpr == '2.8':
        # Replace pink pixels with red (BGR format)
        image[pink_mask > 0] = [0, 0, 255]
        print("pixels changed to red")
    elif gpr == '3.0':
        # Replace pink pixels with black pixels (BGR format)
        image[pink_mask > 0] = [255, 0, 0]
        print("pixels changed to black")
    else:
        # Replace pink pixels with black pixels (BGR format)
        image[pink_mask > 0] = [255, 255, 0]
        print("pixels kept green")

    # Save the modified image as input_image_path + "new"
    # cv2.imwrite(input_image_path + "new", image)
    cv2.imwrite(output_image_path, image)

# Example usage:
input_folder = "gpr_test"  # Replace with your input image path
output_folder = "gpr_test_new"

# Check if there are values between underscores
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)

        image_name = os.path.basename(input_image_path)
        values_between_underscores = image_name.split('_')[1]

        if values_between_underscores:
            try:
                # change_mask_colour(input_image_path, output_image_path, values_between_underscores)
                if values_between_underscores == '2.8':
                    print("changing " + filename + " red")
                    change_pink_to_red(input_image_path, output_image_path)
                    print("changed " + filename + " red")
                elif values_between_underscores == '3.0':
                    print("changing " + filename + " black")
                    change_pink_to_purple(input_image_path, output_image_path)
                    print("changed " + filename + " black")
                elif values_between_underscores == '2.1':
                    print("changing " + filename + " blue")
                    change_pink_to_cyan(input_image_path, output_image_path)
                    print("changed " + filename + " blue")
                elif values_between_underscores == '1.6':
                    print("changing " + filename + " brown")
                    change_pink_to_brown(input_image_path, output_image_path)
                    print("changed " + filename + " brown")
                else:
                    keep_pink(input_image_path, output_image_path)


            except Exception as e:
                print(f"Error processing")

print("Mask colours changed!")