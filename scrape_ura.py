from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.common.action_chains import ActionChains

condo_names = ['DAHLIA DRIVE']
driver = webdriver.Chrome()

def scrape_condo_info(condo_name):
    # Go to the URA website
    driver.get("https://www.ura.gov.sg/maps/?service=MP")

    # Wait for the search box to load and enter the condominium name
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "us-s-txt"))
    )
    search_box.send_keys(condo_name)
    search_box.send_keys(Keys.RETURN)

    # Wait for the address list to load and select the first address
    first_address = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-sr-item"))
    )
    first_address.click()

    # wait and click 'See Other Services'
    see_other_services_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-ip-svcs-l2-other-services"))
    )
    see_other_services_button.click()

    # click explore development site
    explore_dev_site_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-svcs-l1card-template0"]/div'))
    )
    explore_dev_site_button.click()

    # wait and click 'Redevelop site'
    redevelop_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[1]'))
    )
    redevelop_tab.click()

    # GPR
    gpr_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[2]/div[1]/div[2]'))
    )
    print(f'Gross Plot Ratio for {condo_name}: {gpr_value.text}')

    # building height control restrictions
    height_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[3]/div[1]/div[2]'))
    )
    print(f'Building height control restrictions for {condo_name}: {height_value.text}')

    # maximum dwelling units
    max_dwelling_units = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[6]/div[5]/div/div'))
    )
    print(f'Maximum dwelling units for {condo_name}: {max_dwelling_units.text}')

    # landscape replacement area
    lra = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[7]/div[5]/div/div'))
    )
    print(f'Landscape replacement area(LRA) for {condo_name}: {lra.text}')

    # wait and click on 'See more'
    see_more_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div[1]/div[4]/div[2]/div[2]/a'))
    )
    see_more_link.click()

    # setback requirements
    WebDriverWait(driver, 10).until(
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

            print(f'Road: {road_name}, Category: {road_category}, Residential Road Buffer: {residential_road_buffer}')
            index += 2
        except NoSuchElementException:
            # Exit the loop if the element isn't found, which likely means we've processed all cards
            break

    # section to take ss
    # click layers tab
    layers = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "us-map-layers"]'))
    )
    layers.click()

    # wait and locate location pin
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".leaflet-marker-icon"))
    )
    marker_icon = driver.find_elements(By.CSS_SELECTOR, ".leaflet-marker-icon")[0]

    # ensure location pin is in view
    driver.execute_script("arguments[0].scrollIntoView();", marker_icon)

    # zoom in to maximum zoon
    actions = ActionChains(driver)
    actions.move_to_element(marker_icon)
    for _ in range(50):
        actions.send_keys(Keys.ADD)
    actions.perform()

    # relocate location pin avoid StaleElementReferenceException
    marker_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-marker-icon.leaflet-zoom-animated"))
    )

    # ensure location pin is in view again
    driver.execute_script("arguments[0].scrollIntoView();", marker_icon)

    # ss of site
    driver.save_screenshot('screenshot_area.png')

    # toggle on the site plan view
    site_layout_toggle = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-ol-lyr-content"]/div[2]/div[2]/div/div[2]/div[2]/label/span'))
    )
    site_layout_toggle.click()

    # force sleep so it can apply the site plan view
    time.sleep(5)

    # ss of site plan
    driver.save_screenshot('screenshot_site_plan.png')

    # zoom in again for better site view
    # toggle on OneMap
    onemap_toggle = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-ol-lyr-content"]/div[2]/div[1]/div/div[2]/div[2]/label/span'))
    )
    onemap_toggle.click()
    marker_icon = driver.find_elements(By.CSS_SELECTOR, ".leaflet-marker-icon")[0]
    driver.execute_script("arguments[0].scrollIntoView();", marker_icon)
    actions = ActionChains(driver)
    actions.move_to_element(marker_icon)

    zoom_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-map"]/div[3]/div[3]/div[2]/a[1]'))
    )
    for _ in range(4):
        zoom_in_button.click()

    marker_icon = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-marker-icon.leaflet-zoom-animated"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", marker_icon)
    time.sleep(5)
    driver.save_screenshot('screenshot_site_plan_zoom.png')

# iterate over the condominium names
for condo_name in condo_names:
    scrape_condo_info(condo_name)

driver.quit()
