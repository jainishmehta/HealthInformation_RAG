import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <a> tags (links) in the parsed HTML
        links = soup.find_all('a')
        
        # Print each link's text and href attribute
        for link in links:
            print(f"Text: {link.text} | URL: {link.get('href')}")
    else:
        print(f"Failed to retrieve page: {response.status_code}")

# Example usage:
if __name__ == "__main__":
    url = 'https://example.com'  # Replace with the URL you want to scrape
    scrape_website(url)
