from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import os

# List of condominium names
condo_names = []
index_names = []
to_remove = []
scraped_data = []
no_result = False
special_control = False

# clear the contents of the folders Area, Site plan and Zoom
folders = ['Screenshots/Area', 'Screenshots/Site plan', 'Screenshots/Zoom']
for foldername in folders:
    for filename in os.listdir(foldername):
        if filename == None:
            break
        file_path = os.path.join(foldername, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

csv_file_path = 'condo_data_new_v2.csv'

# Open the CSV file and read its contents
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Iterate through each row and extract the value from the first column
    for row in csv_reader:
        if row:  # Check if the row is not empty
            zero_column_value = row[0] # Index 0 corresponds to the first column
            first_column_value = row[1]  
            index_names.append(zero_column_value)
            condo_names.append(first_column_value)
# delete the first element in condo_names
condo_names.pop(0)
index_names.pop(0)
# row filter
condo_names = condo_names[1900:]
index_names = index_names[1900:]

# # for scraping at specific indexes
# indices = [11, 21]  #for index 12 and 22
# condo_names = [condo_names[i] for i in indices]
# index_names = [index_names[i] for i in indices]

# Initialize Selenium WebDriver (Chrome)
driver = webdriver.Chrome()

# Function to check if there is no result
def no_result_check(condo_name):
    global no_result
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='list-group us-sr-group']/div[@class='us-sr-noresult']"))
        )
        if "No matching result" in element.text:
            to_remove.append(condo_name)
            print(to_remove)
            no_result = True
    except:
        pass
    return no_result

# Function to check if there is special control
def special_control_check(condo_name):
    global special_control
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='us-c-ip']/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[1]"))
        )
        if "Special Controls" in element.text:
            to_remove.append(condo_name)
            special_control = True
            print(to_remove)
    except:
        pass
    return special_control

# Function to scrape the data for a single condominium
def scrape_condo_info(index_name, condo_name):
    global no_result
    global special_control

    # Dictionary to store the data for the current condominium
    condo_data = {'Index': ' ', 'Address': ' ', 'GPR': ' ', 'Area': ' ', 'Dwelling Units': ' ', 'LRA': ' ', 'Height control': ' ', 'Max dwelling units': ' ', 
                'Road setback': ' '}
    condo_data['Index'] = index_name
    condo_data['Address'] = condo_name

    print("Checking " + condo_name)
    # Go to the URA website
    driver.get("https://www.ura.gov.sg/maps/?service=MP")

    # Wait for the search box to load and enter the condominium name
    search_box = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "us-s-txt"))
    )
    search_box.send_keys(condo_name)
    search_box.send_keys(Keys.RETURN)
    
    # Wait for the 'clear' icon to be clickable and click it
    clear_icon = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, 'us-s-clear'))
    )
    no_result = False
    no_result_check(condo_name)
    # print(no_result)
    if no_result == True:
        return
    
    else:
        try:
            # Wait for the address list to load and select the first address
            first_address = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/div[1]"))
                # EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-sr-item"))
            )
            first_address.click()
            print('Address clicked')
        except NoSuchElementException:
            print("Element not found!")
        except TimeoutException:
            print("Operation timed out!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        try:
            # wait and click 'See Other Services'
            see_other_services_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-ip-svcs-l2-other-services"))
            )
            see_other_services_button.click()

            # Click 'Explore Development Site'
            explore_dev_site_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#us-svcs-l1card-template0"))
            )
            explore_dev_site_button.click()
            print('Explore development site clicked')
        except Exception as e:
            try:
                # wait and click 'See Other Services'
                see_other_services_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-ip-svcs-l2-other-services"))
                )
                see_other_services_button.click()

                # Click 'Explore Development Site'
                explore_dev_site_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#us-svcs-l1card-template0"))
                )
                explore_dev_site_button.click()
                print('Explore development site clicked')
            except NoSuchElementException:
                print("Element not found!")
            except TimeoutException:
                print("Operation timed out!")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        try:
            view_site_info_tab = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.us-svcs-site-l1-option'))
            )
            view_site_info_tab.click()

            # click 'Development Information'
            development_info_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[5]/div[1]/div[2]'))
            )
            development_info_button.click()
            print('Development information 1 clicked')
        except Exception as e:
            try:
                # click 'Development Information'
                development_info_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[5]/div[1]/div[2]'))
                )
                development_info_button.click()
                print('Development information 2 clicked')
            except NoSuchElementException:
                print("Element not found!")
            except TimeoutException:
                print("Operation timed out!")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        try:
            # gross floor area
            gross_floor_area = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div/div[1]/div[2]'))
            )
            condo_data['GPR'] = gross_floor_area.text
            print(f'Gross floor area for {condo_name}: {gross_floor_area.text}')

        except NoSuchElementException:
            print("Element not found!/dh")
        except TimeoutException:
            print("Operation timed out!/dh")
        except Exception as e:
            print(f"An unexpected error occurred: {e}/dh")

        try:
            # site area
            site_area = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div/div[2]/div[2]'))
            )
            condo_data['Area'] = site_area.text
            print(f'Site area for {condo_name}: {site_area.text}')

            # building height
            building_height = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div/div[3]/div[2]'))
            )
            print(f'Building height for {condo_name}: {building_height.text}')

            # no of dwelling units
            dwelling_units = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div/div[4]/div[2]'))
            )
            condo_data['Dwelling Units'] = dwelling_units.text
            print(f'Number of dwelling units for {condo_name}: {dwelling_units.text}')
        except NoSuchElementException:
            print("Element not found!")
        except TimeoutException:
            print("Operation timed out!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        try:  
            # Wait and click 'Redevelop Site'
            redevelop_tab = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[1]'))
            )
            redevelop_tab.click()
            print('Redevelop site clicked')

            special_control = False
            special_control_check(condo_name)
            print(special_control)
            if special_control == True:
                return
            
            else:
                print('Searching for GPR')
                # GPR
                gpr_value = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[2]/div[1]/div[2]'))
                )
                condo_data['GPR'] = gpr_value.text
                print(f'Gross Plot Ratio for {condo_name}: {gpr_value.text}')

                # building height control restrictions
                height_value = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[3]/div[1]/div[2]'))
                )
                condo_data['Height control'] = height_value.text
                print(f'Building height control restrictions for {condo_name}: {height_value.text}')

                # maximum dwelling units
                max_dwelling_units = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[6]/div[5]/div/div'))
                )
                condo_data['Max dwelling units'] = max_dwelling_units.text
                print(f'Maximum dwelling units for {condo_name}: {max_dwelling_units.text}')

                # landscape replacement area
                lra = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[7]/div[5]/div/div'))
                )
                condo_data['LRA'] = lra.text
                print(f'Landscape replacement area (LRA) for {condo_name}: {lra.text}')

                # wait and click on 'See more'
                see_more_link = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div[1]/div[4]/div[2]/div[2]/a'))
                )
                see_more_link.click()
                # print('See more clicked')

                # setback requirements
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="us-svcs-site-dev-pp-sb-rrl-card"]/div/div[1]'))
                )

                index = 1
                while True:
                    try:
                        road_name_xpath = f'//*[@id="us-svcs-site-dev-pp-sb-rrl-card"]/div/div[1]/div[{index}]/div[1]'
                        # // *[ @ id = "us-svcs-site-dev-pp-sb-rrl-card"] / div / div[1] / div[1] / div[1]
                        # // *[ @ id = "us-svcs-site-dev-pp-sb-rrl-card"] / div / div[1] / div[3] / div[1]
                        road_category_xpath = f'//*[@id="us-svcs-site-dev-pp-sb-rrl-card"]/div/div[1]/div[{index}]/div[2]/div'
                        # // *[ @ id = "us-svcs-site-dev-pp-sb-rrl-card"] / div / div[1] / div[1] / div[2] / div
                        # // *[ @ id = "us-svcs-site-dev-pp-sb-rrl-card"] / div / div[1] / div[3] / div[2] / div
                        residential_road_buffer_xpath = f'//*[@id="us-svcs-site-dev-pp-sb-rrl-card"]/div/div[1]/div[{index+1}]/div[2]'
                        # // *[ @ id = "us-svcs-site-dev-pp-sb-rrl-card"] / div / div[1] / div[2] / div[2]
                        # // *[ @ id = "us-svcs-site-dev-pp-sb-rrl-card"] / div / div[1] / div[4] / div[2]

                        road_name = driver.find_element(By.XPATH, road_name_xpath).text
                        road_category = driver.find_element(By.XPATH, road_category_xpath).text
                        residential_road_buffer = driver.find_element(By.XPATH, residential_road_buffer_xpath).text

                        condo_data['Road setback'] = [road_name, road_category, residential_road_buffer]

                        print(f'Road: {road_name}, Category: {road_category}, Residential Road Buffer: {residential_road_buffer}')
                        index += 2
                    except NoSuchElementException:
                        # Exit the loop if the element isn't found, which likely means we've processed all cards
                        break
        except NoSuchElementException:
            print("Element not found!")
        except TimeoutException:
            print("Operation timed out!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            


        # section to take ss
        try:
            # toggle on setback marking
            site_layout_toggle = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="us-svcs-site-rdev-pp-sb-crrl"]/div[2]/label/span'))
            )
            site_layout_toggle.click()
            # print('Site layout toggle 1 clicked')

            # click layers tab
            layers = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "us-map-layers"]'))
            )
            layers.click()
            # print("Layers clicked")

            # wait and locate location pin
            WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".leaflet-marker-icon"))
            )
            marker_icon = driver.find_elements(By.CSS_SELECTOR, ".leaflet-marker-icon")[0]
            # ensure location pin is in view
            driver.execute_script("arguments[0].scrollIntoView();", marker_icon)
            # zoom in to maximum zoon
            zoom_in_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="us-map"]/div[3]/div[3]/div[2]/a[1]'))
            )
            for _ in range(10):
                zoom_in_button.click()
                # print('Zoom 1 clicked')
            # relocate location pin avoid StaleElementReferenceException
            marker_icon = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-marker-icon.leaflet-zoom-animated"))
            )
            # ensure location pin is in view again
            driver.execute_script("arguments[0].scrollIntoView();", marker_icon)

            toggle_element = driver.find_element(By.XPATH, '//*[@id="us-ol-lyr-content"]/div[2]/div[2]/div/div[2]/div[3]')
            driver.execute_script("arguments[0].style.display = 'none';", marker_icon)
            if 'd-none' in toggle_element.get_attribute('class'):
                # toggle on the site plan view
                site_layout_toggle = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="us-ol-lyr-content"]/div[2]/div[2]/div/div[2]/div[2]/label/span'))
                )
                site_layout_toggle.click()
                time.sleep(3)
                # save the screenshot with file name condo_name
                driver.save_screenshot(f'{index_name}_area.png')
                #  move the screenshot to the folder 'Screenshots'
                os.rename(f'{index_name}_area.png', f'Screenshots/Area/{index_name}_area.png')
                print('Screenshot area saved 1')
            else:
                time.sleep(3)
                # save the screenshot with file name condo_name
                driver.save_screenshot(f'{index_name}_area.png')
                os.rename(f'{index_name}_area.png', f'Screenshots/Area/{index_name}_area.png')
                print('Screenshot area saved 2')

            # toggle off the site plan view
            site_layout_toggle = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="us-ol-lyr-content"]/div[2]/div[2]/div/div[2]/div[2]/label/span'))
            )
            site_layout_toggle.click()
            # print('Site layout toggle 2 clicked')

            # toggle on OneMap
            onemap_toggle = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="us-ol-lyr-content"]/div[2]/div[1]/div/div[2]/div[2]/label/span'))
            )
            onemap_toggle.click()
            # print('Onemap toggle clicked')

            # force sleep so it can apply the site plan view
            time.sleep(3)

            # ss of site plan
            # save the screenshot with file name condo_name
            driver.save_screenshot(f'{index_name}_site_plan.png')
            os.rename(f'{index_name}_site_plan.png', f'Screenshots/Site plan/{index_name}_site_plan.png')
            print('Screenshot site plan saved')

            # zoom in again for better site view
            marker_icon = driver.find_elements(By.CSS_SELECTOR, ".leaflet-marker-icon")[0]
            driver.execute_script("arguments[0].scrollIntoView();", marker_icon)
            zoom_in_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="us-map"]/div[3]/div[3]/div[2]/a[1]'))
            )
            for _ in range(4):
                zoom_in_button.click()
                # print('Zoom 2 clicked')

            marker_icon = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-marker-icon.leaflet-zoom-animated"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", marker_icon)
            time.sleep(5)
            # save the screenshot with file name condo_name
            driver.save_screenshot(f'{index_name}_site_plan_zoom.png')
            os.rename(f'{index_name}_site_plan_zoom.png', f'Screenshots/Zoom/{index_name}_zoom.png')
            print('Screenshot site plan zoom saved')

        except NoSuchElementException:
            print("Element not found!")
        except TimeoutException:
            print("Operation timed out!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # print condo_name scraped
        print(f'{condo_name} scraped!')
    
        # Append the condo data dict to the scraped_data list
        scraped_data.append(condo_data)
    
# Iterate over the condominium names and scrape the info for each
for index_name, condo_name in zip(index_names, condo_names):
    scrape_condo_info(index_name, condo_name)

print(scraped_data)

# After scraping, write the data to a CSV file
with open('scraped_condo_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = list(scraped_data[0].keys())
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(scraped_data)

print('Scraping complete!')
print(to_remove)

# Close the WebDriver
driver.quit()
