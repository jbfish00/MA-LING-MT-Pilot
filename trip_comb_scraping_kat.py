import requests
from bs4 import BeautifulSoup
import time
import os

# Base URL for the Georgian scriptures page (update this URL as needed)
BASE_URL_DC = "https://www.churchofjesuschrist.org/study/scriptures/dc-testament?lang=kat"
BASE_URL_PGP = "https://www.churchofjesuschrist.org/study/scriptures/pgp?lang=kat"

# Define headers to mimic a browser request
HEADERS = {
    "User-Agent": (
        "Edg/110.0.1587.57"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ka,ka;q=0.9",
    "Connection": "keep-alive"
}


def scrape_scripture_text(scripture_url):
    """
    Scrape the scripture text from the given scripture URL.
    The function looks for a container that holds the scripture text. 
    You may need to update the class or id selector based on the actual page structure.
    """
    response = requests.get(scripture_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve {scripture_url}")
        return ""
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Example: Assume the scripture text is within a <div> with a class 'scripture-text'
    text_elements = soup.find_all("div", class_="scripture-text")
    if not text_elements:
        # If not found, try another selector that might contain the text
        text_elements = soup.find_all("div", id="scriptureContent")
    
    # Combine all text elements, stripping extra whitespace
    text = "\n".join(elem.get_text(strip=True) for elem in text_elements)
    return text

def save_text(text, filename):
    """Save the scraped text to a UTF-8 encoded file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved scripture text to {filename}")

def main():
    # Create a directory to store scraped texts
    os.makedirs("georgian_scriptures", exist_ok=True)
    
    scripture_links = get_scripture_links(BASE_URL)
    print("Found scripture links:", scripture_links)
    
    for link in scripture_links:
        # Construct the full URL if the link is relative
        if link.startswith("http"):
            full_url = link
        else:
            full_url = "https://www.churchofjesuschrist.org" + link
        
        print("Scraping:", full_url)
        
        # Scrape the main scripture page text
        text = scrape_scripture_text(full_url)
        if text:
            # Create a filename based on the URL path
            # For example, /study/scriptures/pgp?lang=kat => study_scriptures_pgp_lang=kat.txt
            filename = link.strip("/").replace("/", "_").replace("?", "_").replace("=", "_") + ".txt"
            filepath = os.path.join("georgian_scriptures", filename)
            save_text(text, filepath)
        else:
            print(f"No text found at {full_url}")
        
        # Be respectful: sleep between requests
        time.sleep(2)

if __name__ == "__main__":
    main()