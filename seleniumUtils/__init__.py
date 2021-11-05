import pathlib
import os
import threading, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def init_drive(headless=None):
    current_directory_path = pathlib.Path(__file__).parent.absolute()
    chrome_driver_path = os.path.join(
        current_directory_path, "./drivers/chromedriver")
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options, executable_path=chrome_driver_path)

def wait_by_name(driver, element_name):
    while True:
        try:
            element = driver.find_elements_by_name(element_name)
            if element: break
            time.sleep(1)
        except Exception as e:
            time.sleep(1)

def wait_by_class(driver, element_class):
    while True:
        try:
            element = driver.find_elements_by_xpath(
        "//div[contains(@class,'"+element_class+"')]")
            if element: break
            time.sleep(1)
        except Exception as e:
            time.sleep(1)