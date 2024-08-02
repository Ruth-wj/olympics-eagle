import logging
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from user_agents import user_agents


def setup_chrome_webdriver(chrome_driver_manager: ChromeDriverManager) -> webdriver:
    options = Options()
    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en")
    driver = webdriver.Chrome(service=Service(chrome_driver_manager), options=options)
    driver.delete_all_cookies()
    return driver


def click_cookie_banner(driver: webdriver) -> None:
    only_necessary_button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cmpboxbtn.cmpboxbtnno.cmptxt_btn_no"))
    )
    only_necessary_button.click()


def find_event_dates(driver: webdriver) -> list:
    offer_elements = driver.find_elements(
        By.CSS_SELECTOR, "div.listing-item.theme-text-color.listing-item-clickable"
    )
    return offer_elements

def wait_for_page_to_load(driver: webdriver) -> None:
    """bad bad bad todo proper failure modes here"""
    while True:
        page_state = driver.execute_script('return document.readyState;')
        if page_state == "complete":
            break

def get_offer_states(driver: webdriver) -> list:
    element_css = 'div.listing-event-status.theme-text-highlight-color.theme-interaction-color.hidden-xs.hidden-sm.listing-event-price > span'
    try:
        logging.info("checking for offer states")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pageContent"]/main/section[3]/div/serp-widget/search-results/div/product-listing/div[1]/serp-filter/div[2]/div[2]/section/button[1]')))
        elements = driver.find_elements(
            By.CSS_SELECTOR, element_css
        )
    except Exception as e:
        logging.info("failed to find offer states")
        logging.info(e)
        elements = []
    return [element.text for element in elements]

def get_offer_links(driver: webdriver) -> list:
    # Locate all <a> elements
    a_elements = driver.find_elements(By.TAG_NAME, 'a')

    # Extract href attributes
    hrefs = [element.get_attribute('href') for element in a_elements]
    string_hrefs = [href for href in hrefs if isinstance(href, str)]
    relevent_hrefs = [href for href in string_hrefs if "/tickets/all/" in href]
    return relevent_hrefs

def refresh_on_access_denied(driver: webdriver) -> None:
    try:
        h1_element = driver.find_element(By.TAG_NAME, 'h1')
        if h1_element.text == "Access Denied":
            logging.info("Access Denied detected. Refreshing ...")
            driver.refresh()
            time.sleep(1)
    except Exception as e:
        if "Unable to locate element" in e.message:
            return
        else:
            raise e
