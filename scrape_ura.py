from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# List of condominium names
condo_names = ['DAHLIA DRIVE']

# Initialize Selenium WebDriver (Chrome)
driver = webdriver.Chrome()


# Function to scrape the data for a single condominium
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

    # Wait for the 'See Other Services' button to be clickable and click it
    see_other_services_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-ip-svcs-l2-other-services"))
    )
    see_other_services_button.click()

    # click explore development site
    explore_dev_site_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-svcs-l1card-template0"]/div'))
    )
    explore_dev_site_button.click()

    # Wait for the 'Redevelop Site' tab to be clickable and click it
    redevelop_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[1]'))
    )
    redevelop_tab.click()

    # Wait for the GPR (Gross Plot Ratio) value to load and print it
    gpr_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[2]/div[1]/div[2]'))
    )
    print(f'Gross Plot Ratio for {condo_name}: {gpr_value.text}')

    #building height control restrictions
    height_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[3]/div[1]/div[2]'))
    )
    print(f'Building height control restrictions for {condo_name}: {height_value.text}')

    #maximum dwelling units
    max_dwelling_units = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[6]/div[5]/div/div'))
    )
    print(f'Maximum dwelling units for {condo_name}: {max_dwelling_units.text}')

    #landscape replacement area
    lra = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[7]/div[5]/div/div'))
    )
    print(f'Landscape replacement area(LRA) for {condo_name}: {lra.text}')

    # Wait for the 'See more' link to be clickable and click it
    see_more_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[5]/div[2]/div[1]/div[4]/div[2]/div[2]/a'))
    )
    see_more_link.click()

    # Wait for the setback requirements section to load
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

# Iterate over the condominium names and scrape the info for each
for condo_name in condo_names:
    scrape_condo_info(condo_name)

# Close the WebDriver
driver.quit()
