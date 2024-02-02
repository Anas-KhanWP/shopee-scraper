from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

# Create a ChromeOptions object to configure the browser
options = webdriver.ChromeOptions()

# Start the Chrome browser with the configured options
driver = webdriver.Chrome()

def goToUrl(driver, url):
    driver.get(url)

def languageSelector(driver):
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"Language => {soup}")

        # Find the button with text "English" using XPath
        english_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'English')]"))
        )

        english_button.click()
    except:
        print("No Option")
def logIn(email, password):
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"Login => {soup}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='loginKey']"))
        ).send_keys(email)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        ).send_keys(password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]"))
        ).click()

        time.sleep(5)
    except:
        print("No Login Option")
def parseHtml(driver, url):
    driver.get(url)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    print(f"Main => {soup}")

def scrape(driver, url, email, password):
    goToUrl(driver, url)

    languageSelector(driver)

    logIn(email, password)

    parseHtml(driver, url)

    time.sleep(40)

    _div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flex.items-center.idLK2l.page-product__breadcrumb"))
    )

    # Categories
    _breadcrumbs = _div.find_elements(By.CLASS_NAME, "EtYbJs")

    # (1, 2, 3) Will be in here
    category = []

    for cat in _breadcrumbs:
        _cat = cat.text
        category.append(cat)

    print(f"Categories => {category}")

    _productDiv = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "DXQgih"))
    )

    # (4) Product Name
    _productName = _productDiv.find_element(By.TAG_NAME, "span").text

    print(f"Product Name => {_productName}")

    # Rating Parent
    _ratingDiv = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flex.asFzUa"))
    )

    _rating_stars_div = _ratingDiv.find_element(By.XPATH, "//div[@class='F9RHbS dQEiAI']")
    total_ratings_div = _ratingDiv.find_element(By.XPATH, "//div[@class='F9RHbS']")
    total_sold = _ratingDiv.find_element(By.XPATH, "//div[@class='AcmPRb']")

    # (5) Rating Stars
    _rating_stars = _rating_stars_div.text
    print(f"Rating Stars => {_rating_stars}")

    # (6) Total Ratings
    totalRating = total_ratings_div.text
    print(f"Total Ratings => {totalRating}")

    # (7) Total SOld
    sold = total_sold.text
    print(f"Total Products Sold => {sold}")


scrape(driver, "https://shopee.co.th/product/453309769/16810604722", "webdev195@gmail.com", "Taimoor1729")