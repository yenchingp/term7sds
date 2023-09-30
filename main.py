from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# List of condominium names
condo_names = []
to_remove = []
status = True

csv_file_path = 'condo_data_new_v2.csv'

# Open the CSV file and read its contents
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Iterate through each row and extract the value from the first column
    for row in csv_reader:
        if row:  # Check if the row is not empty
            first_column_value = row[0]  # Index 0 corresponds to the first column
            condo_names.append(first_column_value)
# delete the first element in condo_names
condo_names.pop(0)

# Initialize Selenium WebDriver (Chrome)
driver = webdriver.Chrome()

def no_result_check(condo_name):
    global status
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='list-group us-sr-group']/div[@class='us-sr-noresult']"))
        )
        if "No matching result" in element.text:
            to_remove.append(condo_name)
            status = False
    except:
        pass
    return status

# Function to scrape the data for a single condominium
def scrape_condo_info(condo_name):
    global status
    # Go to the URA website
    driver.get("https://www.ura.gov.sg/maps/?service=MP")

    # Wait for the search box to load and enter the condominium name
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "us-s-txt"))
    )
    search_box.send_keys(condo_name)
    search_box.send_keys(Keys.RETURN)
    
    # Wait for the 'clear' icon to be clickable and click it
    clear_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'us-s-clear'))
    )
    status = True
    no_result_check(condo_name)
    print(status)
    if status == False:
        return
    else:
        # Wait for the address list to load and select the first address
        first_address = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[2]/div[1]"))
            # EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-sr-item"))
        )
        first_address.click()

        # # Wait for the 'See Other Services' button to be clickable and click it
        # see_other_services_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, ".us-ip-svcs-l2-other-services"))
        # )
        # see_other_services_button.click()

        # # Wait for the 'Explore Development Site' to be clickable and click it
        # explore_dev_site_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#us-svcs-l1card-template0"))
        # )
        # explore_dev_site_button.click()

        # # Wait for the 'Redevelop Site' tab to be clickable and click it
        # redevelop_tab = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[1]'))
        # )
        # redevelop_tab.click()

        # # Wait for the GPR (Gross Plot Ratio) value to load and print it
        # gpr_value = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="us-c-ip"]/div[3]/div/div[2]/div/div[2]/div[1]/div[5]/div[2]/div[1]/div[2]/div[1]/div[2]'))
        # )
        # print(f'Gross Plot Ratio for {condo_name}: {gpr_value.text}')

        clear_icon.click()
    


# Iterate over the condominium names and scrape the info for each
for condo_name in condo_names:
    scrape_condo_info(condo_name)
print(to_remove)
# Close the WebDriver
driver.quit()
