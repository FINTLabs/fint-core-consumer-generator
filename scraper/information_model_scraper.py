from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def update_information_model():
    version = input("Information model version: ")

    # Set up the Chrome options
    options = Options()
    options.add_argument('--headless')

    # Set up the web driver with the Chrome options
    driver = webdriver.Chrome(options=options)

    # Navigate to the website
    url = f'https://informasjonsmodell.felleskomponent.no/docs?v=v{version}'
    driver.get(url)

    # Wait for 30 seconds for the page to load
    print("Waiting 30 seconds for the page to load")
    time.sleep(30)
    # Print the HTML content of the page
    with open('./information_model.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

    # Close the web driver
    driver.quit()