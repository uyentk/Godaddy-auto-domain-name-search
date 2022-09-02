from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
import time
import pandas as pd
from fake_useragent import UserAgent

url = "https://www.godaddy.com/"
PATH = "C:\Program Files (x86)\chromedriver.exe"

ua = UserAgent(use_cache_server=False, fallback='Your favorite Browser')
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_argument(f'user-agent={ua}')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(PATH, options= options, service = Service(ChromeDriverManager().install()))
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.maximize_window()

action = ActionChains(driver)
driver.get(url)

# fillbox = driver.find_element(By.NAME, 'domainToCheck')
# fillbox.clear()
# fillbox.send_keys("abc.com")

# Change the language of the website
xpaths = ["//span[contains(text(),'Việt Nam - Tiếng Việt')]", "//strong[contains(text(),'United States')]"]

for i in xpaths:
    action.click(driver.find_element(By.XPATH, i))
    action.perform()
    time.sleep(3)

# Input domain
input_df = pd.read_csv("Godaddy-auto-domain-name-search/assets/input.csv", header=None)
output_df = pd.DataFrame({}, columns= ["Domain Name", "Status", "Price", "URL"])

for url in input_df[0]:
    fillbox = driver.find_element(By.NAME, 'domainToCheck')
    fillbox.clear()
    fillbox.send_keys(url)
    time.sleep(5)
    action.click(driver.find_element(By.XPATH, "//button[@type = 'Submit']"))
    action.perform()
    time.sleep(10)

    try:
        driver.find_element(By.XPATH,"//span[contains(text(), 'is available')]")
        price = driver.find_element(By.XPATH,"//span[@data-cy='exact-match-price-main']").text
        try: 
            button = driver.find_element(By.XPATH,"//button[@data-cy='exact-match-add-to-cart-button']")
        except NoSuchElementException:
            try: 
                button = driver.find_element(By.XPATH,"//button[@data-cy='exact-match-make-offer-button']")
            except NoSuchElementException:
                pass
        data = [url, button.text, price, ""]
    except NoSuchElementException:
        data = [url, "Taken", "", ""]

    output_df.loc[len(output_df)] = data 
    print(output_df)
    driver.back()
    time.sleep(5)

print(output_df)  
output_df.to_csv("Godaddy-auto-domain-name-search\src\output.csv")