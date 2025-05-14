import requests  
from bs4 import BeautifulSoup  
import time  
import re  
import os  
  
# Base URL  
base_url = "https://www.light*novel*globe.com"  
  
# List of starting URLs (first chapters of each novel)  
start_urls = [  
    "/novel/NovelTitle Bblah-245/chapter-1-27061855",  
    "/novel/Blah another Novel title just get the URL from first chapter and put it here1258/chapter-1-09061431"
]  
  
# Function to scrape a chapter  
def scrape_chapter(url, folder_name):  
    try:  
        headers = {  
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'  
        }  
        response = requests.get(url, headers=headers, verify=False)  
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')  
  
        # Extract chapter title and content  
        title_tag = soup.find('h1')  
        content_tag = soup.find('div', class_='chapter-content')  
  
        if not title_tag or not content_tag:  
            print(f"Failed to find title or content at {url}")  
            return None  
  
        title = title_tag.text.strip()  
        content = content_tag.text.strip()  
  
        # Sanitize filename: remove invalid characters, including newlines  
        filename = re.sub(r'[\\/*?:"<>|\n\r]', "_", f"{title}.txt").replace(' ', '_')  
        file_path = os.path.join(folder_name, filename)  
  
        # Save to file  
        with open(file_path, 'w', encoding='utf-8') as file:  
            file.write(title + "\n\n" + content)  
  
        print(f'Successfully saved {title}')  
  
        # Find the "Next" button  
        next_button = soup.find('a', class_='button nextchap')  
        if next_button:  
            next_url = next_button.get('href')  
            full_next_url = base_url + next_url if not next_url.startswith("http") else next_url  
            return full_next_url  
        else:  
            print("No more chapters found.")  
            return None  
    except Exception as e:  
        print(f'Failed to scrape {url}: {e}')  
        return None  
  
# Iterate through each novel  
for start_url in start_urls:  
    # Extract novel name for folder naming  
    novel_name = start_url.split('/')[2]  
    folder_name = novel_name.replace('-', '_')  
    os.makedirs(folder_name, exist_ok=True)  
  
    # Start scraping from the first chapter  
    current_url = base_url + start_url  
    while current_url:  
        current_url = scrape_chapter(current_url, folder_name)  
        time.sleep(1)  # Be polite and don't overload the server  
  
print("Scraping completed.")  
