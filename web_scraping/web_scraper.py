from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to initialize the WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")  # Run in headless mode
    
    chrome_options.binary_location = '/mnt/c/Program Files/Google/Chrome/Application/chromedriver.exe'

    try:
        # Install ChromeDriver using WebDriver Manager
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

    return driver

# Function to scrape search results for a specific disease
def scrape_search_results(driver, disease):
    base_url = "https://www.mayoclinic.org"
    search_url = f"{base_url}/diseases-conditions/search-results?q={disease.replace(' ', '%20')}"
    driver.get(search_url)
    time.sleep(2)  # Wait for the page to load

    # Find the first search result and click on it
    try:
        first_result = driver.find_element(By.CSS_SELECTOR, 'a.search-results-link')
        first_result.click()
        time.sleep(2)  # Wait for the page to load
        return driver.page_source
    except Exception as e:
        print(f"Error finding or clicking the search result: {e}")
        return None

# Function to scrape tips from a disease page
def scrape_disease_tips(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    tips_section = soup.find('div', class_='content')
    
    if not tips_section:
        return None
    
    tips = tips_section.find_all('li')  # Adjust the tag/class based on the actual HTML structure
    
    tips_list = [tip.get_text(strip=True) for tip in tips]
    return tips_list

# List of diseases to scrape
diseases = [
    'diabetes'
]

# Initialize the WebDriver
driver = init_driver()

# Initialize a list to store the data
data = []

# Loop through each disease, search for results, and scrape tips
for disease in diseases:
    print(f"Scraping tips for: {disease}")
    page_source = scrape_search_results(driver, disease)
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
