from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import json
import time
import random

# Main Function
def main():

    # Declare product_page_urls list and product_data list to store data in form list of dictionaries
    product_data_dict = {}
    review_urls = []

    # Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Using headless=False because most of the times it triggers captcha, manually solve it while the program is running also it is easier to debug
        context = browser.new_context()
        page = context.new_page()

        # Open JSON file containing product URLs
        with open(r"output\amazon_product_page_url.json", 'r', encoding='utf-8') as json_file:
            product_urls = json.load(json_file)
            # For loop urls in json file to scrape product data and review URLs
            for url in product_urls[:5]:
                loading_page(page, url['url']) # Load page
                scraping_page_data_and_reviews_url(page, product_data_dict, review_urls) # Scrape product data and review URLs

        # Close Playwright
        browser.close()

    # Write the data to a JSON file
    with open(r'output\amazon_review_page_url.json', 'w', encoding='utf-8') as json_file:
        json.dump(review_urls, json_file, ensure_ascii=False, indent=4)

    # Function to store product data in a JSON file
    storing_product_data(product_data_dict)

# Product Details and Review URLs Scraping Function from Product URLs
def scraping_page_data_and_reviews_url(page, product_data_dict, review_urls):
    
    # Parse HTML
    soup = BeautifulSoup(page.content(), "lxml")

    # Get product asin from page URL using regex pattern
    asin_pattern = re.search(r"/dp/([^/?&]+)", page.url)
    asin = asin_pattern.group(1).strip()
    # Get product rating
    rating_div = soup.find("div", {'id': 'averageCustomerReviews'})
    rating = rating_div.find("span", {'class': 'a-size-base a-color-base'}).text.strip()
    # Get product brand information
    try:
        brand_information_list = [] # List to store brand information data from different divs , then join them into a string 
        brand_information_container = soup.find('div', {'class': 'a-section a-spacing-small a-spacing-top-small'}) # Div container containing brand information data
        brand_information_data = brand_information_container.find_all('tr') # Find all trs containing brand information data
        for data in brand_information_data: # For loop to get brand information data from each tr
            brand_information_text = data.text.strip()
            brand_information_list.append(brand_information_text) # Append brand information data to brand_information_list
        brand_information = ', '.join(brand_information_list) # Join brand_information_list into a string
    except:
        brand_information = None # If brand information is not found, set it to None
    # Get product technical information
    try:
        technical_information_list = [] # List to store technical information data from different table rows , then join them into a string
        # Different technical information tables have different ids, so we use a for loop to get the technical information data from each table. Some page may use only one id while others may use two or three ids.
        technical_information_ids = [
            'productDetails_techSpec_section_1',
            'productDetails_techSpec_section_2',
            'productDetails_detailBullets_sections1'
        ]
        # For loop to get technical information data from each table
        for technical_information_id in technical_information_ids:
            try:
                technical_information_table = soup.find('table', {'id': f'{technical_information_id}'}) # Find table containing technical information data
                technical_information_rows = technical_information_table.find_all('tr') # Find all table rows containing technical information data
                for row in technical_information_rows:
                    technical_information_text = row.text.strip() # Get technical information data from each table row
                    clean_technical_information_text = technical_information_text.replace("  \n                \u200e"," ") # Clean technical information data
                    technical_information_list.append(clean_technical_information_text) # Append technical information data to technical_information_list
            except:
                pass
        technical_information = ', '.join(technical_information_list) # Join technical_information_list into a string
    except:
        technical_information = None # If technical information is not found, set it to None
    # Get product review page URL by finding the review page tag and extracting the href attribute then adding it to the base URL
    review_page_tag = soup.find("a", class_="a-link-emphasis a-text-bold")
    review_page_url = f"https://www.amazon.com{review_page_tag.get('href')}"
    
    # Store product data in product_data_dict
    product_data_dict[asin] = {"rating":rating, "brand_information":brand_information, "technical_information":technical_information}

    # Append review page URL to review_urls
    review_urls.append({"asin":asin, "url":review_page_url})

def storing_product_data(product_data_dict):
    # Declare selected_items list to store data in form list of dictionaries then write it to a JSON file
    selected_items = []
    # Open JSON file containing product data
    with open(r"output\amazon_product_data_1.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # For loop to merge product data
        for item in data:
            asin = item.get('asin') # Get asin from product data to use as a key to get product data from product_data_dict
            offers_pattern = r"\d+ offer.*$" # Get offers number from offers text using regex pattern
            offers = int(re.sub(offers_pattern, '', item.get('offers'))) # Get offers text from product data
            rating = product_data_dict.get(asin, {}).get("rating") # Get product rating from product_data_dict using asin as a key
            rating = float(rating) if rating is not None else None # Convert rating to float if it is not None
            # Merge product data by create a new dictionary
            selected_item = {'asin':item.get('asin'),
                            'title':item.get('title'),
                            'rank':int(item.get('rank').replace('#', '')),
                            'price':float(item.get('price').replace('$', '')),
                            'rating_volume':int(item.get('rating_volume')),
                            'offers':offers,
                            'offers_bool':item.get('offers_bool'),
                            'rating':rating,
                            'brand_information':product_data_dict.get(asin, {}).get("brand_information", None), # Get product brand information from product_data_dict using asin as a key
                            'technical_information':product_data_dict.get(asin, {}).get("technical_information", None) # Get product technical information from product_data_dict using asin as a key
                            }
            selected_items.append(selected_item)
    # Write the merged data to a new JSON file
    with open(r"output\amazon_product_data_2.json", 'w', encoding='utf-8') as merged_file:
        json.dump(selected_items, merged_file, ensure_ascii=False, indent=4)

def loading_page(page, url):

    # Max attempts
    max_attempts = 3

    # For loop to try loading page
    for i in range(max_attempts):
        
        # Page Load
        page.goto(url)
        page.wait_for_load_state()
        time.sleep(random.randint(5, 10)) # Most of the times it triggers captcha, manually solve it while the program is sleeping
        page.click('#productTitle') # Click product title

        # Check if page is loaded
        if page.wait_for_selector('#nav-logo-sprites'): # Using the Amazon logo as a selector to check if page is loaded

            # Trigger javascript elements to load all page content
            for i in range(10):
                page.keyboard.press('PageDown')
                time.sleep(1)
            page.keyboard.press('End')
            page.wait_for_load_state()
            break
        # If page is not loaded, try again
        else:
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()
