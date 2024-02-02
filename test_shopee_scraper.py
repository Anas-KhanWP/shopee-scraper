# File name: test_shopee_scraper.py
from seleniumbase import BaseCase
import pytest

@pytest.mark.usefixtures("setUpClass")
class ShopeeScraperTest(BaseCase):

    @classmethod
    def setUpClass(cls):
        super(ShopeeScraperTest, cls).setUpClass()

    def test_scrape(self):
        self.go_to("https://shopee.co.th/product/453309769/16810604722")
        self.languageSelector()
        self.logIn("webdev195@gmail.com", "Taimoor1729")
        self.parseHtml("https://shopee.co.th/product/453309769/16810604722")
        self.sleep(40)

        _div = self.wait_for_element_present('.flex.items-center.idLK2l.page-product__breadcrumb')

        # Categories
        _breadcrumbs = _div.find_elements('.EtYbJs')

        # (1, 2, 3) Will be in here
        category = []

        for cat in _breadcrumbs:
            _cat = cat.text
            category.append(cat)

        print(f"Categories => {category}")

        _productDiv = self.wait_for_element_present('.DXQgih')

        # (4) Product Name
        _productName = _productDiv.find_element('span').text

        print(f"Product Name => {_productName}")

        # Rating Parent
        _ratingDiv = self.wait_for_element_present('.flex.asFzUa')
        _rating_stars_div = _ratingDiv.find_element('.F9RHbS.dQEiAI')
        total_ratings_div = _ratingDiv.find_element('.F9RHbS')
        total_sold = _ratingDiv.find_element('.AcmPRb')

        # (5) Rating Stars
        _rating_stars = _rating_stars_div.text
        print(f"Rating Stars => {_rating_stars}")

        # (6) Total Ratings
        totalRating = total_ratings_div.text
        print(f"Total Ratings => {totalRating}")

        # (7) Total Sold
        sold = total_sold.text
        print(f"Total Products Sold => {sold}")

    def goToUrl(self, url):
        self.open(url)

    def languageSelector(self):
        try:
            self.wait_for_element_present('//button[contains(text(), "English")]').click()
        except Exception as e:
            print(f"No Option: {e}")

    def logIn(self, email, password):
        try:
            self.wait_for_element_present('//input[@name="loginKey"]').send_keys(email)
            self.wait_for_element_present('//input[@name="password"]').send_keys(password)
            self.wait_for_element_present('//button[contains(text(), "Log In")]').click()
            self.sleep(5)
        except Exception as e:
            print(f"No Login Option: {e}")

    def parseHtml(self, url):
        self.goToUrl(url)
        soup = self.get_beautiful_soup()
        print(f"Main => {soup}")

    def scrape(self, url, email, password):
        self.goToUrl(url)

        self.languageSelector()

        self.logIn(email, password)

        self.parseHtml(url)

        self.sleep(40)

        _div = self.wait_for_element_present('.flex.items-center.idLK2l.page-product__breadcrumb')

        # Categories
        _breadcrumbs = _div.find_elements('.EtYbJs')

        # (1, 2, 3) Will be in here
        category = []

        for cat in _breadcrumbs:
            _cat = cat.text
            category.append(cat)

        print(f"Categories => {category}")

        _productDiv = self.wait_for_element_present('.DXQgih')

        # (4) Product Name
        _productName = _productDiv.find_element('span').text

        print(f"Product Name => {_productName}")

        # Rating Parent
        _ratingDiv = self.wait_for_element_present('.flex.asFzUa')
        _rating_stars_div = _ratingDiv.find_element('.F9RHbS.dQEiAI')
        total_ratings_div = _ratingDiv.find_element('.F9RHbS')
        total_sold = _ratingDiv.find_element('.AcmPRb')

        # (5) Rating Stars
        _rating_stars = _rating_stars_div.text
        print(f"Rating Stars => {_rating_stars}")

        # (6) Total Ratings
        totalRating = total_ratings_div.text
        print(f"Total Ratings => {totalRating}")

        # (7) Total Sold
        sold = total_sold.text
        print(f"Total Products Sold => {sold}")

# Run the test class
ShopeeScraperTest().test_scrape()
