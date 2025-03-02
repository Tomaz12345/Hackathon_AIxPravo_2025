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

import sipo, euipo, wipo


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

if __name__ == "__main__":
    #driver = setup_driver(headless=True)
    brand = "Nike"
    goods_services = "construction"
    try:
        driver = setup_driver(headless=True)
        euipo.search_brand(driver, brand, goods_services)
    except:
        print("Huston, we have a problem")
    driver = setup_driver(headless=True)
    sipo.search_brand(driver, brand, goods_services)
    driver = setup_driver(headless=True)
    wipo.search_brand(driver, brand, goods_services)
    driver.quit()
    print("Done")