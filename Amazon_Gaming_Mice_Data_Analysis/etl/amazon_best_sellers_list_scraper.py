from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import json
import time
import random

# Main Function
def main():

    # Declare product_page_urls list and product_data list
    # List to store data in form list of dictionaries
    product_page_urls = []
    product_data = []

    # Playwright sequence
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Using headless=False because most of the times it triggers captcha, manually solve it while the program is running also it is easier to debug
        context = browser.new_context()
        page = context.new_page()

        # Urls of top 100 best seller gaming pc mice pages
        best_seller_pages = [
            "https://www.amazon.com/best-sellers-video-games/zgbs/videogames/402052011/ref=zg_bs_pg_1_videogames?_encoding=UTF8&pg=1",
            "https://www.amazon.com/best-sellers-video-games/zgbs/videogames/402052011/ref=zg_bs_pg_2_videogames?_encoding=UTF8&pg=2"
        ]

        # For loop pages in best_seller_pages and scrape product_page_urls and product_data
        for page_url in best_seller_pages:
            loading_page(page, page_url)
            scraping_page(page, product_page_urls, product_data)

        # Store product_page_urls in a JSON file
        with open(r'output\amazon_product_page_url.json', 'w', encoding='utf-8') as json_file:
            json.dump(product_page_urls, json_file, ensure_ascii=False, indent=4)

        # Store product_data in a JSON file
        with open(r'output\amazon_product_data_1.json', 'w', encoding='utf-8') as json_file:
            json.dump(product_data, json_file, ensure_ascii=False, indent=4)

        # Close Playwright
        browser.close()

def loading_page(page, url):

    # Max attempts
    max_attempts = 3

    # For loop to try loading page
    for i in range(max_attempts):
        
        # Page Load
        page.goto(url)
        page.wait_for_load_state()
        time.sleep(random.randint(5, 10)) # Most of the times it triggers captcha, manually solve it while the program is sleeping
        page.click('#zg_banner_subtext') # Click on the banner

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

# Product Details Scraping Function from Top 100
def scraping_page(page, product_page_urls, product_data):
    
    # Parse HTML
    soup = BeautifulSoup(page.content(), "lxml")

    # Get catalogue and container using CSS selectors
    catalogue_container = soup.find('div', {'class': 'p13n-gridRow _cDEzb_grid-row_3Cywl'}) # Div tag of the product catalogue
    product_cards = catalogue_container.findAll('div', {'class': 'a-cardui _cDEzb_grid-cell_1uMOS expandableGrid p13n-grid-content'}) # CSS selector of each product card

    # For loop product_cards and scrape product_page_urls and product_data
    for product_card in product_cards:

        # Extract the title

        # These are the variance CSS selector of the title tag
        title_classes = [
                '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1',
                '_cDEzb_p13n-sc-css-line-clamp-4_2q2cc',
                '_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y'
            ]
        # For loop title_classes to find the title tag
        for title_class in title_classes:
                title_tag = product_card.find('div', {'class': title_class})
                if title_tag:
                    title = title_tag.text.strip()

        # Extract the URL
        product_title_a_tag = product_card.find('a', {'class': 'a-link-normal'})
        product_url = f"https://www.amazon.com{product_title_a_tag['href']}"

        # Extract the product ID from the product URL
        product_id = re.search(r'/dp/(.*?)/', product_title_a_tag['href'])

        # Get price and offers

        # These are the variance CSS selector of the price tag
        price_tag_classes = [
            'a-size-base a-color-price', # Price tag when there is no offer
            'a-color-secondary' # Price tag when there is an offer
        ]

        # For loop price_tag_classes to find the price tag
        for tag_class in price_tag_classes:
            price_tag = product_card.find('span', {'class': tag_class})
            
            # If price_tag is found, extract the price
            if price_tag:
                price = price_tag.text.strip()

                # If there is an offer, remove the offer text
                starting_price = re.search(r'\d+ offers from ', price) # Regex to find the offer text
                if starting_price:
                    price = re.sub(r'\d+ offers from ', '', price)
            
                # If there is an offer, extract the offer
                if tag_class == 'a-color-secondary':
                    try:
                        offers_child_tag = product_card.find('span', {'class': 'a-color-secondary'})
                        offers = offers_child_tag.find_parent('a').text.strip()
                        offers_bool = True
                    except:
                        pass
                else:
                    offers = None
                    offers_bool = False        

        # Extract the product rank
        rank_tag = product_card.find('span', {'class': 'zg-bdg-text'})
        rank = rank_tag.text.strip()

        # Extract the product rating volume
        rating_volume_tag = product_card.find('span', {'class': 'a-size-small'})
        rating_volume = rating_volume_tag.text.strip()

        # Add the product page URL to the product_page_urls list as a dictionary
        product_page_urls.append({"asin": product_id.group(1), "url": product_url})

        # Add the product data to the product_data list as a dictionary
        product_data.append({"asin": product_id.group(1), "title": title, "rank": rank, "price": price, "rating_volume": rating_volume, "offers": offers, "offers_bool": offers_bool})

if __name__ == "__main__":
    main()