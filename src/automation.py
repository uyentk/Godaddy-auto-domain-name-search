from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
import time
import pandas as pd

url = "https://www.godaddy.com/"
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(PATH, options= options, service = Service(ChromeDriverManager().install()))
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.maximize_window()

action = ActionChains(driver)
driver.get(url)

fillbox = driver.find_element(By.NAME, 'domainToCheck')
fillbox.clear()
fillbox.send_keys("abc.com")

# Change the language of the website
xpaths = ["//span[contains(text(),'Việt Nam - Tiếng Việt')]", "//strong[contains(text(),'United States')]"]

for i in xpaths:
    action.click(driver.find_element(By.XPATH, i))
    action.perform()
    time.sleep(3)

# Input domain
input_df = pd.read_csv("Godaddy-auto-domain-name-search/assets/input.csv", header=None)

for url in input_df[0]:
    fillbox = driver.find_element(By.NAME, 'domainToCheck')
    fillbox.clear()
    fillbox.send_keys(url)
    time.sleep(5)
    action.click(driver.find_element(By.XPATH, "//button[@type = 'Submit']"))
    action.perform()
    time.sleep(3)
    driver.back()

    
