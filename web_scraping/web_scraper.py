from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import pandas as pd
import time

# Function to initialize the WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--incognito")
    #chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    
    try:
        print("sds")
        # Install ChromeDriver using WebDriver Manager
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

    return driver



def search_and_navigate(driver, disease):
    base_url = f"https://www.mayoclinic.org/search/search-results?q={disease}"
    driver.get(base_url)
    
    try:
        time.sleep(5)
        # Find all search results
        search_results = driver.find_elements(By.CSS_SELECTOR, 'a.azsearchlink')
        
        # Iterate through the search results and find the one closest to "Diagnosis and treatment"
        best_match = None
        print(search_results)
        for result in search_results:
            if "Diagnosis and treatment" in result.text:
                best_match = result
                break

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


# Function to scrape tips from a disease page
def scrape_disease_tips(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    tips_section = soup.find('div', class_='content')
    
    if not tips_section:
        return None
    
    tips = tips_section.find_all('li')  # Adjust the tag/class based on the actual HTML structure
    print(tips)
    tips_list = [tip.get_text(strip=True) for tip in tips]
    return tips_list

# List of diseases to scrape
diseases = [
    'diabetes'
]

# Initialize the WebDriver
driver = init_driver()

if driver:
    # Initialize a list to store the data
    data = []

    # Loop through each disease, search for results, and scrape tips
    for disease in diseases:
        print(f"Scraping tips for: {disease}")
        page_source = search_and_navigate(driver, disease)
        if page_source:
            tips = scrape_disease_tips(page_source)
            if tips:
                for tip in tips:
                    data.append({'disease': disease, 'tip': tip})
            time.sleep(1)  # Add delay to avoid overwhelming the server

    # Close the WebDriver
    driver.quit()

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('mayo_clinic_wellness_tips.csv', index=False, encoding='utf-8')

    print("Scraping completed and data saved to mayo_clinic_wellness_tips.csv")
else:
    print("Failed to initialize the WebDriver. Exiting the script.")
