import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the Selenium WebDriver (e.g., using Chrome)
driver = webdriver.Chrome()

# Base URL of the website
base_url = "https://dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list.html"

driver.get(base_url)

# Find all anchor elements with the specified class
links = driver.find_elements(By.CSS_SELECTOR, '.cmp-list__item-link')

# Extract the aria-label attributes
aria_labels = [link.get_attribute('aria-label') for link in links]

print(aria_labels)
# Wait for 5 seconds before closing
time.sleep(15)
# Close the WebDriver
driver.quit()
