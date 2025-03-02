from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import uuid
import os
import re
from utils import save


def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")  # Updated for newer Chrome versions
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use webdriver-manager to handle chromedriver automatically
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver



def search_brand(driver, brand, goods_services):
    print(brand)
    print(goods_services)
    url = "https://www3.wipo.int/madrid/monitor/en/#"
    driver.get(url)
    data_to_save = []

    advanced_search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='modeText' and text()='advanced search']")))
    advanced_search.click()

    if brand is not None:
        input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BRAND_input")))
        input_field.clear()
        input_field.send_keys(brand)

    if goods_services is not None:
        input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "GS_ALL_input")))
        driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
        input_field.clear()
        input_field.send_keys(goods_services)

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='noPrint searchButton bigButton ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-secondary']/span[text()='search']"))
    )
    search_button.click()
    time.sleep(2)

    data = []
    total_num = 0

    while True:
        # Get all rows from the table, excluding the first one (header)
        rows = driver.find_elements(By.XPATH, "//table[@id='gridForsearch_pane']/tbody/tr[position()>1]")
        time.sleep(2)

        for i, row in enumerate(rows):
            print(total_num)
            total_num += 1
            # Extract the desired data from each row
            try:
                temp_rez = row.find_elements(By.XPATH, ".//td[@role='gridcell' and @aria-describedby='gridForsearch_pane_STATUS']//img[contains(@src, 'active.png')]")
                time.sleep(2)
                if temp_rez == []:
                    continue

                entry = {}
                brand_text = row.find_element(By.XPATH, ".//td[@role='gridcell' and @aria-describedby='gridForsearch_pane_BRAND']").text.strip()
                entry["brand"] = brand_text
                owner = row.find_element(By.XPATH, ".//td[@role='gridcell' and @aria-describedby='gridForsearch_pane_HOL']").text.strip()
                entry["owner"] = owner
                irn = row.find_element(By.XPATH, ".//td[@role='gridcell' and @aria-describedby='gridForsearch_pane_IRN']").text.strip()
                entry["ID"] = irn
                nc = row.find_element(By.XPATH, ".//td[@role='gridcell' and @aria-describedby='gridForsearch_pane_NC']").text.strip()
                entry["NIC"] = nc

                # Extract image (if available)
                image_element = row.find_elements(By.XPATH, ".//td[@aria-describedby='gridForsearch_pane_IMG']//img")
                if image_element:
                    image = image_element[0].get_attribute("src")
                else:
                    image = "No image"
                entry["image"] = image

                # Print the extracted data
                print(f"Brand: {brand}, Owner: {owner}, IRN: {irn}, NC: {nc}, Image: {image}", )
                data.append(entry)

            except Exception as e:
                print("Error extracting data from row:", e)
        
        # Check if the "Next" button is disabled
        try:
            pagination_container = driver.find_element(By.CLASS_NAME, "results_pager")
            disabled_next_button = pagination_container.find_elements(
                By.XPATH, ".//span[contains(@class, 'ui-state-disabled') and contains(@class, 'ui-button-icon-only')]//span[contains(@class, 'ui-icon-triangle-1-e')]"
            )
            next_button = pagination_container.find_elements(By.XPATH, ".//a[contains(@class, 'ui-button-icon-only') and not(contains(@class, 'ui-state-disabled'))]//span[contains(@class, 'ui-icon-triangle-1-e')]")
            if next_button == []:
                break

            next_button[0].click()
            time.sleep(2)
            
        except:
            # If "Next" button isn't found or an error occurs, exit the loop
            print("Next button not found, exiting.")
            break
    

    print(data)


    # save the data to a csv file
    if brand is not None and goods_services is not None:
        # with random id added
        filename = f"wipo_{brand}_{goods_services}_{uuid.uuid4()}.csv"
    elif brand is not None:
        filename = f"wipo_{brand}_{uuid.uuid4()}.csv"
    else:
        filename = f"wipo_{goods_services}_{uuid.uuid4()}.csv"
    
    print(f"Saving data to {filename}")
    save(filename, data)



if __name__ == "__main__":
    driver = setup_driver(headless=True)
    try:
        #results = search_brand(driver, "Nike", "footwear")
        #results = search_brand(driver, "Apple", "vision")
        results = search_brand(driver, "Petrol", None)
    finally:
        driver.quit()