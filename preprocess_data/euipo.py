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
    url = "https://euipo.europa.eu/eSearch/#advanced/trademarks"
    driver.get(url)
    data_to_save = []

    elements = driver.find_elements(By.CLASS_NAME, "cdelete")
    for element in elements:
        element.click()
    
    if brand is not None:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-criteria-name='MarkVerbalElementText']"))
        )
        element.click()

        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='MarkVerbalElementText']"))
        )
        time.sleep(0.5)
        input_field.clear()
        time.sleep(0.5)
        input_field.send_keys(brand)
        input_field.send_keys(Keys.RETURN)
    
    if goods_services is not None:
        pass
    #'''if True:
        goods_services_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-criteria-name='GoodsServicesDescription']"))
        )
        goods_services_link.click()  # Click the link

        # Wait for the input field for "GoodsServicesDescription" to be visible and interactable
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='GoodsServicesDescription']"))
        )

        # Clear and send keys
        input_field.clear()  # Clear the field
        time.sleep(0.5)  # Optional: slight delay to ensure clearing is completed

        # Send the desired input
        input_field.send_keys(goods_services)  # Enter text
        input_field.send_keys(Keys.RETURN)  # Press Return to submit the form #'''
    
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "doSearchBt"))
    )

    search_button.click()

    num = 0

    number_of_results = -1
    search_info = driver.find_element(By.CSS_SELECTOR, 'div.searchInfo.pull-right').text

    # Use regular expression to extract the first number (the search results count)
    match = re.search(r'(\d+)', search_info)

    if match:
        # Extracted number is in the first group of the match
        number_of_results = match.group(1)
        print(number_of_results)


    while True:
        # Find all the boxes inside the search results
        boxes = driver.find_elements(By.CSS_SELECTOR, ".search-results-boxes .box.light")
        if (not number_of_results == -1) and (num >= int(number_of_results)):
            break

        for i, box in enumerate(boxes):
            print(num)
            num += 1

            # Now check if the status icon is "LIVE" or "DEAD"
            status_icon = box.find_elements(By.CSS_SELECTOR, "i.iconMarkStatus")
            if len(status_icon) > 0:
                entry = {}
                icon_class = status_icon[0].get_attribute("class")
                
                if "CSD_8" in icon_class:  # LIVE/REGISTRATION
                    #print("Processing this trademark...")
                    
                    # Extracting Trademark Number, Nice Classification, and Owner Name
                    try:
                        trade_mark_number = box.find_element(By.XPATH, ".//dt[text()='Trade mark number']/following-sibling::dd").get_attribute("innerHTML")
                        #print(f"Trade mark number: {trade_mark_number}")
                        entry["ID"] = trade_mark_number

                        # brand name
                        #element = driver.find_element(By.CSS_SELECTOR, 'a.detailsBt')
                        #name = element.text.split('-')[1].strip()
                        name = box.find_element(By.CSS_SELECTOR, 'a.detailsBt').get_attribute("innerHTML").split("\n")[2].lstrip(' ')[2:]
                        entry["brand"] = name
                        
                        # Nice Classification
                        #nice_classification = WebDriverWait(driver, 10).until(
                        #    EC.visibility_of_element_located((By.XPATH, ".//dt[text()='Nice Classification']/following-sibling::dd"))
                        #).text
                        nice_classification = box.find_element(By.XPATH, ".//dt[text()='Nice Classification']/following-sibling::dd").get_attribute("innerHTML")
                        #print(f"Nice Classification: {nice_classification}")
                        entry["NIC"] = nice_classification
                        
                        # Owner Name
                        #owner_name = WebDriverWait(driver, 10).until(
                        #    EC.visibility_of_element_located((By.XPATH, ".//dt[text()='Owner name']/following-sibling::dd"))
                        #).text
                        owner_name = box.find_element(By.XPATH, ".//dt[text()='Owner name']/following-sibling::dd").get_attribute("innerHTML")
                        #print(f"Owner Name: {owner_name}")
                        owner_name = owner_name.replace("\n", " ")
                        entry["owner"] = owner_name
                    
                    except Exception as e:
                        print("Error extracting details:", e)

                    # Check if the box has an image thumbnail
                    thumbnail = box.find_element(By.CSS_SELECTOR, ".thumbnail")
                    link_elements = thumbnail.find_elements(By.XPATH, ".//a[@class='designimage itemImage']")
                    
                    # Check if it contains an image
                    if not link_elements:
                        #print("No image")
                        entry["image"] = "No Image"
                    else:
                        # Get the image URL (assuming it's in the <img> tag inside the thumbnail div)
                        img = link_elements[0].find_element(By.TAG_NAME, "img")
                        img_url = img.get_attribute('src')
                        entry["image"] = img_url
                        #print("Image found:", img_url)
                        
                        # Save the image
                        '''img_name = img_url.split("/")[-1]
                        img_path = os.path.join(image_dir, img_name)
                        
                        # Download the image
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                        }
                        img_data = requests.get(img_url, headers=headers).content
                        with open(img_path + ".jpg", 'wb') as file:
                            file.write(img_data)
                        print(f"Image saved as {img_name}")'''
                    data_to_save.append(entry)
                elif "CSD_14" in icon_class:  # DEAD/REGISTRATION
                    pass
                    #print("Not processing this trademark...")
                else:
                    pass
                    #print("Unknown status, skipping...")
        
        # Check if the "Next" button is available and clickable
        try:
            next_page = driver.find_element(By.XPATH, "//a[contains(@class, 'next-page') and @title='Next']")
            #time.sleep(2)
            driver.execute_script("""
                var parent = arguments[0].parentElement;
                parent.style.display = 'block';
                parent.style.visibility = 'visible';
                parent.style.opacity = '1';
                parent.style.position = 'relative';
            """, next_page)
            #time.sleep(2)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
            #time.sleep(2)
            driver.execute_script("arguments[0].parentElement.scrollIntoView(true);", next_page)
            #time.sleep(2)
            driver.execute_script("arguments[0].click();", next_page)
            #next_page = driver.find_element(By.XPATH, "//a[contains(@class, 'next-page') and @title='Next']")
            #time.sleep(2)
            #WebDriverWait(driver, 10).until(
            #    EC.visibility_of_element_located((By.XPATH, "//a[@class='next-page' and @title='Next']"))
            #)
            #time.sleep(2)
            #WebDriverWait(driver, 10).until(
            #    EC.element_to_be_clickable((By.XPATH, "//a[@class='next-page' and @title='Next']"))
            #)
            #time.sleep(2)
            #next_page = driver.find_elements(By.XPATH, "//a[@class='next-page' and @title='Next']")[0]
            #driver.execute_script("arguments[0].click();", next_page)
            #next_page.click()  # Click the "Next" button to go to the next page
                # total
            
            #else:
            #print("Going to the next page...")

        except Exception as e:
            print("No more pages or unable to click 'Next':", e)
            break  # Break the loop if there's no "Next" button or it isn't clickable

    
    # save the data to a csv file
    if brand is not None and goods_services is not None:
        # with random id added
        filename = f"euipo_{brand}_{goods_services}_{uuid.uuid4()}.csv"
    elif brand is not None:
        filename = f"euipo_{brand}_{uuid.uuid4()}.csv"
    else:
        filename = f"euipo_{goods_services}_{uuid.uuid4()}.csv"
    
    print(f"Saving data to {filename}")


    # save the data to a csv file
    save(filename, data_to_save)


if __name__ == "__main__":
    driver = setup_driver(headless=True)
    try:
        #results = search_brand(driver, "Nike", "footwear")
        #results = search_brand(driver, "Nike", "footwear")
        results = search_brand(driver, "Apple", None)
    finally:
        driver.quit()