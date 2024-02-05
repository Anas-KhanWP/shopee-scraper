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
import csv
from datetime import datetime
import os

options = webdriver.ChromeOptions()
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

    # (8) Price
    _price = _ratingDiv.find_element(By.XPATH, "//div[@class='G27FPf']")
    final_price = _price.text
    print(f"Price => {final_price}")

    # (9) Discount Amount
    _discount = _ratingDiv.find_element(By.XPATH, "//div[@class='o_z7q9']")
    _discount_amount = _discount.text
    print(f"Discount Amount => {_discount_amount}")

    # (11) Pieces Available
    parent_div = driver.find_element(By.XPATH, "//div[@class='flex items-center']")
    _pieces_div = parent_div.find_element(By.XPATH, ".//div[last()]")
    _pieces_available = _pieces_div.text
    print(f"Pieces available => {_pieces_available}")

    # (12) Video Link
    video_element = driver.find_element(By.CLASS_NAME, "tpgcVs")
    src_attribute = ""
    if video_element:
        src_attribute = video_element.get_attribute("src")
        print(f"Video Link => {src_attribute}")
    else:
        print("No video link")

    # (13) Image Links:
    images = []
    image_elements = driver.find_elements(By.CLASS_NAME, "IMAW1w")
    for image in image_elements:
        image_for_url = image.find_element(By.XPATH, "//img[@class='IMAW1w']")
        image_link = image_for_url.get_attribute("src")
        print(f"Image url => {image_link}")
        images.append(image_link)

    # Generate current date and time for the output file name
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"extracted_info_{current_datetime}.csv"

    # Check if the file already exists
    if os.path.isfile(output_filename):
        # Open the existing file in append mode
        mode = 'a'
    else:
        # Create a new file
        mode = 'w'

    # Write to CSV
    with open(output_filename, mode, newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write header only if it's a new file
        if mode == 'w':
            csvwriter.writerow(["Category", "Product Name", "Rating Stars", "Total Ratings", "Total Sold",
                                "Price", "Discount Amount", "Pieces Available", "Video Link", "Image Links"])

        # Write data
        csvwriter.writerow([category, _productName, _rating_stars, totalRating, sold,
                            final_price, _discount_amount, _pieces_available, src_attribute, images])


scrape(driver, "https://shopee.co.th/product/453309769/16810604722", "webdev195@gmail.com", "Taimoor1729")
