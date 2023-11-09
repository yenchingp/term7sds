import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from urllib.parse import quote
import time


# Define your directories
input_directory = 'mapbox_rd/mapbox_input' # Replace with the path to your HTML files
output_directory = 'mapbox_rd_ss/input'  # Replace with the path to save screenshots
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Set up the Selenium WebDriver
# The example here uses ChromeDriverManager which automatically downloads the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Loop through all files in the input directory
for file_name in os.listdir(input_directory):
    # if file_name + '.png' exists
    if os.path.isfile(os.path.join(output_directory, file_name + '.png')):
        # print("File already exists!")
        continue
    else:
        # Construct the full file path
        file_path = os.path.join(input_directory, file_name)
        print(file_path)
        # Open the HTML file with the WebDriver
        driver.get(f'file:///C:/Users/zyjy1/Documents/SUTD%20Stuff/Term%207/Spatial%20Design%20Studio/term7sds/{file_path}')

        # Give some time for the browser to render any JavaScript if needed
        # driver.implicitly_wait(10)
        time.sleep(1.5)

        # Construct the output file path
        screenshot_path = os.path.join(output_directory, file_name + '.png')
        
        # Take a screenshot of the page
        driver.save_screenshot(screenshot_path)

# Clean up: close the browser window
driver.quit()