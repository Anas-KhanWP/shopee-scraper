import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 

xpaths_to_print = {
            '1':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/a[2]',
            '2':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/a[3]',
            '3':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/a[4]',
            'main_title':'//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[1]/span',
           'startrating':'//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[2]/button[1]/div[1]',
           'rating':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[2]/button[2]/div[1]',
            '7':'//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[2]/div/div[1]',
            'price range':'//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[3]/div/div/section/div/div[2]/div[1]',
            'discount':'//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[3]/div/div/section/div/div[2]/div[2]',
            '10':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[4]/div/div[1]/section/div/div/div[2]',
            '11':'//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[4]/div/div[2]/div/section[2]/div/div[2]',
            '12':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[1]/div[1]/div[1]/div/div/div[2]/video',
            '13':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[1]/div[1]/div[2]/div[1]/div/div[1]/picture/img',
            '14':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[1]/div[1]/div[2]/div[2]/div/div[1]/picture/img',
            '15':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[1]/div[1]/div[2]/div[3]/div/div[1]/picture/img',
            '16':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[1]/div[1]/div[2]/div[4]/div/div[1]/picture/img',
            '17':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[1]/div[1]/div[2]/div[5]/div/div[1]/picture/img',                     
            '18':'/html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/section[1]/section[2]/div/div[4]/div/section/div/div[2]/div[2]/div[2]/div[2]/div/div',
}


# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=["Link"] + list(xpaths_to_print.keys()))

def print_element(xpath, code ,link,iterator):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        val = int(code)
        
        if 12 <= val <= 17:
            # For elements with keys 12 to 17, get the src attribute
            src_attribute = element.get_attribute("src")
            print(f"Content of {xpath} src attribute: {src_attribute}")
            result_df[code][iterator] = src_attribute
    
        else:
            # For other elements, get the text content
            print(f"Content of {xpath}: {element.text}")
            result_df[code][iterator] = element.text
            
      
    except:
        print(f"Could not find element with XPath {xpath}: ")
        result_df.loc[len(result_df)] = [link] + [None]
        pass

        
excelFile = input("enter url excel file path ==>")
df = pd.read_excel(excelFile)

iterator = 0 
links = df['links']
html_parser =[]
try:
    options = uc.ChromeOptions()
    # options.add_argument("--headless")  # Set to True for headless mode
    options.add_argument("--disable-gpu")
    
    
    driver = uc.Chrome(options=options) 
    for link in links:
        retry_count = 3  # Set the number of retries
        while retry_count > 0:
            try:
                print(link)
                driver.get(link)
                time.sleep(1)
                try:
                    english_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[2]/button'))
                    )
                    english_button.click()
                    time.sleep(2)
                except:
                    pass

                try:
                    login_input = driver.find_element(By.NAME, "loginKey")
                    login_input.send_keys("webdev195@gmail.com")
                    time.sleep(1)

                    password_input = driver.find_element(By.NAME, "password")
                    password_input.send_keys("Taimoor1729")
                    time.sleep(1)

                    login_button = driver.find_element(By.CLASS_NAME, "wyhvVD")
                    login_button.click()
                except:
                    pass

                # Wait for the "page-product" class to be present in the HTML
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "page-product"))
                )
                # Iterate through XPaths and print elements
                for code, xpath in xpaths_to_print.items():
                    print_element(xpath, code, link,iterator)
                    iterator += 1
                # Break out of the loop if successful
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                retry_count -= 1
                if retry_count > 0:
                    print(f"Retrying... {retry_count} attempts remaining.")
                    press = input("Enter any key when captcha is solved ==> ")
                else:
                    print(f"All retry attempts exhausted. Skipping this link.")
                    break    
        

                
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    excel_filename = "shopee_data.xlsx"
    result_df.to_excel(excel_filename, index=False)
    print(f"Results saved to {excel_filename}")
    input("Press enter to exit.....")
