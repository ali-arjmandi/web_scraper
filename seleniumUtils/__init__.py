import pathlib
import os
import threading, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def init_drive(headless=None):
    current_directory_path = pathlib.Path(__file__).parent.absolute()
    chrome_driver_path = os.path.join(
        current_directory_path, "./drivers/win95")
    options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
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

def wait_until_load(driver):
    while True:
        try:
            page_state = driver.execute_script('return document.readyState;')
            if page_state == 'complete': break
            time.sleep(1)
        except:
            time.sleep(1)

def find_by_class_eq(driver, element_class, multi=False):
    elements =  driver.find_elements_by_xpath(".//*[@class='"+ element_class +"']")
    if not len(elements): return
    if multi: return elements
    else: return elements[0]

def find_by_class_includes(driver, element_class, multi=False):
    elements =  driver.find_elements_by_xpath(".//*[contains(@class,'"+element_class+"')]")
    if not len(elements): return
    if multi: return elements
    else: return elements[0]

def find_by_tag(driver, tag, multi=False):
    elements =  driver.find_elements_by_xpath(".//"+tag)
    if not len(elements): return
    if multi: return elements
    else: return elements[0]

def find_by_xpath(driver, xpath, multi=False):
    elements =  driver.find_elements_by_xpath(xpath)
    if not len(elements): return
    if multi: return elements
    else: return elements[0]