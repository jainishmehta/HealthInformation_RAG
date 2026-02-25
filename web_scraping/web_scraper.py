from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from bs4 import BeautifulSoup

import pandas as pd
import time

def init_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless=new") 
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

    return driver

def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept additional cookies')]"))
        )
        accept_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error accepting cookies: {e}")
        pass

def search_and_navigate(driver, disease):
    disease = disease.replace(" ", "_")
    encoded_disease = quote(disease)
    base_url = f"https://www.mayoclinic.org/search/search-results?q={encoded_disease}"
    print(base_url)
    driver.get(base_url)
    accept_cookies(driver)
    try:
<<<<<<< HEAD
        time.sleep(5)
        search_results = driver.find_elements(By.CSS_SELECTOR, 'a.azsearchlink')
        
        # Iterate through the search results and find the one closest to "Diagnosis and treatment"
        best_match = None
        for result in search_results:
            if "Diagnosis and treatment" in result.text:
                best_match = result
                break
=======
        # Find all search results
       time.sleep(5)
       search_results = driver.find_elements(By.CSS_SELECTOR, 'a.azsearchlink')
       print("search_results: ", search_results)
       # Iterate through the search results and find the one closest to "Diagnosis and treatment"
       best_match = None
       for result in search_results:
        if "Diagnosis and treatment" in result.text:
            best_match = result
            break
>>>>>>> e0a04e3 (Updated scraping and rag main to updated import)

        if not best_match:
            # If no exact match is found, find the result that contains either "Diagnosis" or "treatment"
            for result in search_results:
                if "Diagnosis" in result.text or "treatment" in result.text:
                    best_match = result
                    break
        
        # If a match is found, click it
        if best_match:
            best_match.click()
            time.sleep(10)
            return driver.page_source
        else:
            print(f"No relevant result found for {disease}")
            return None

    except Exception as e:
        print(f"Error during the search or navigation: {e}")
        return None

<<<<<<< HEAD

=======
>>>>>>> e0a04e3 (Updated scraping and rag main to updated import)
def scrape_disease_tips(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    tips_section = soup.find('div', class_='content')
    
    if not tips_section:
        return None

    treatment_header = tips_section.find('h2', string='Treatment')
    if not treatment_header:
        return None
<<<<<<< HEAD
=======
    print("treatment_header: ", treatment_header)
    # Find the list that follows the "Treatment" header
>>>>>>> e0a04e3 (Updated scraping and rag main to updated import)
    treatment_list = treatment_header.find_next_sibling('ul')
    print("treatment_list: ", treatment_list)
    if not treatment_list:
        return None
<<<<<<< HEAD
    tips = treatment_list.find_all('li')# Adjust the tag/class based on the actual HTML structure
=======
    # Get all 'li' elements within that list
    tips = treatment_list.find_all('li')
    print("tips: ", tips)
>>>>>>> e0a04e3 (Updated scraping and rag main to updated import)
    tips_list = [tip.get_text(strip=True) for tip in tips]
    print("tips_list: ", tips_list)
    return tips_list


driver = init_driver()

if driver:
    data = []
    base_url = "https://dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list.html"

    driver.get(base_url)
    time.sleep(5)
<<<<<<< HEAD
    # Find all elements
    links = driver.find_elements(By.CSS_SELECTOR, '.cmp-list__item-link')
    diseases = [link.get_attribute('aria-label') for link in links]
    
=======
    links = driver.find_elements(By.CSS_SELECTOR,'a.cmp-navigation__item-link')

    diseases = [link.get_attribute('title') for link in links]
>>>>>>> e0a04e3 (Updated scraping and rag main to updated import)

    print(diseases)
    time.sleep(15)
    for disease in diseases:
        print(f"Scraping tips for: {disease}")

    data = []
    for disease in diseases:
        page_source = search_and_navigate(driver, disease)
        if page_source:
            tips = scrape_disease_tips(page_source)
            if tips:
                for tip in tips:
                    data.append({'disease': disease, 'tip': tip})
<<<<<<< HEAD
            else:
                continue
=======
>>>>>>> e0a04e3 (Updated scraping and rag main to updated import)
            time.sleep(1)
    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv('mayo_clinic_wellness_tips.csv', index=False, encoding='utf-8')

    print("Scraping completed and data saved to mayo_clinic_wellness_tips.csv")
else:
    print("Failed to initialize the WebDriver")

