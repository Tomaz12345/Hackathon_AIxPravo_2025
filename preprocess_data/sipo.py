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
import uuid
from utils import save


total_num = 0


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
    url = "http://www2.uil-sipo.si/"  # Replace with actual URL
    driver.get(url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "disp"))  # Wait for the frame to load
    )

    driver.switch_to.frame("disp")


    link = driver.find_element(By.XPATH, "//a[contains(text(), 'Znamke')]")
    link.click()

    #time.sleep(1)  # Allow page to load

    if brand is not None:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "VTXT"))
        )
        input_vtxt = driver.find_element(By.NAME, "VTXT")
        input_vtxt.send_keys(brand)
    
    if goods_services is not None:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "VGS"))
        )
        input_vlgs = driver.find_element(By.NAME, "VLGS")
        input_vlgs.send_keys(goods_services)

    checkbox = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "I"))  # Finding by 'name' attribute
    )

    # Check if checkbox is already selected
    if not checkbox.is_selected():
        checkbox.click()

    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Izberi']")
    submit_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))  # Adjust based on your next page's element
    )

    #print(driver.page_source)

    def get_extra_data_brand(driver, link):
        link.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Nicejska')]//following-sibling::td/b"))  # Adjust based on your next page's element
        )
        element = driver.find_element(By.XPATH, "//td[contains(text(), 'Nicejska')]//following-sibling::td/b")
        data = element.text
        #driver.back()
        elems = driver.find_elements(By.XPATH, "//td[b[contains(text(), 'Registrirana znamka')]]")
        driver.execute_script("window.history.back();")
        if len(elems) == 0:
            return data, False
        return data, True


    def get_table_data(driver):
        global total_num
        data = []
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@border='0' and @cellspacing='12']"))  # Adjust based on your next page's element
        )
        table = driver.find_element(By.XPATH, "//table[@border='0' and @cellspacing='12']")
        table_elements = table.find_elements(By.TAG_NAME, "tr")
        columns_all = [table_elements[i].find_elements(By.TAG_NAME, "td") for i in range(len(table_elements))]
        columns_texts = []
        columns_images_links = []
        for i, columns in enumerate(columns_all):
            text = []
            try:
                text.append(columns[1].text)
                text.append(columns[2].text)
            except:
                pass
            columns_texts.append(text)
            try:
                columns_images_links.append(columns[-1].find_element(By.TAG_NAME, "img").get_attribute("src"))
            except:
                columns_images_links.append("No Image")
                
        for i, row in enumerate(columns_all):
            columns = row
            print(total_num)
            if len(columns) >= 3:
                entry = {}
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "img"))  # Adjust based on your next page's element
                )
                entry["ID"] = columns_texts[i][0]#columns[1].text.strip()
                temp_text = columns_texts[i][1]#columns[2].text.strip()
                # split by \n
                temp_text = temp_text.split("\n")
                entry["brand"] = temp_text[0]
                # get NIC
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, entry["ID"]))  # Adjust based on your next page's element
                )
                link = driver.find_element(By.LINK_TEXT, entry["ID"])
                entry["owner"] = temp_text[1]
                #img_element = columns[-1].find_elements(By.TAG_NAME, "img")
                #entry["image"] = img_element[0].get_attribute("src") if img_element else "No Image"
                entry["image"] = columns_images_links[i]
                data_extra, rez = get_extra_data_brand(driver, link)
                entry["NIC"] = data_extra
                driver.switch_to.default_content()
                driver.switch_to.frame("disp")
                total_num += 1
                if rez:
                    data.append(entry)
        return data
    
    data = get_table_data(driver)
    driver.switch_to.default_content()
    driver.switch_to.frame("toolbar")
    #WebDriverWait(driver, 10).until(
    #    EC.presence_of_element_located((By.XPATH, "//img[contains(@src, '/f/D.gif') or contains(@src, '/f/DA.gif')]"))  # Adjust based on your next page's element
    #)
    next_icons = driver.find_elements(By.XPATH, "//img[contains(@src, '/f/D.gif') or contains(@src, '/f/DA.gif')]")
    while len(next_icons) > 0:
        next_icons[0].click()
        driver.switch_to.default_content()
        driver.switch_to.frame("disp")
        data.extend(get_table_data(driver))
        driver.switch_to.default_content()
        driver.switch_to.frame("toolbar")
        next_icons = driver.find_elements(By.XPATH, "//img[contains(@src, '/f/D.gif') or contains(@src, '/f/DA.gif')]")
    
    
    #print("Search completed. Now checking for CAPTCHA...")
    
    # save the data to a csv file)
    if brand is not None and goods_services is not None:
        # with random id added
        filename = f"sipo_{brand}_{goods_services}_{uuid.uuid4()}.csv"
    elif brand is not None:
        filename = f"sipo_{brand}_{uuid.uuid4()}.csv"
    else:
        filename = f"sipo_{goods_services}_{uuid.uuid4()}.csv"
    
    print(f"Saving data to {filename}")
    save(filename, data)


if __name__ == "__main__":
    driver = setup_driver(headless=True)
    try:
        #results = search_brand(driver, "Nike", "footwear")
        results = search_brand(driver, "Petrol", None)
    finally:
        driver.quit()
