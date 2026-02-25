import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
base_url = "https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/"

driver.get(base_url)
driver.find_elements_by_class_name('giga bold primary-color push--bottom')
links = driver.find_elements(By.CSS_SELECTOR, '.cmp-list__item-link')
aria_labels = [link.get_attribute('aria-label') for link in links]

print(aria_labels)
time.sleep(15)
driver.quit()
