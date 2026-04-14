from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import json
import time
import random

# Main Function
def main():
    """
    # Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Using headless=False because most of the times it triggers captcha, manually solve it while the program is running also it is easier to debug
        context = browser.new_context()
        page = context.new_page()

        # Opening JSON File containing the product review URLs
        with open(r"output\amazon_review_page_url.json") as json_file:
            product_review_urls = json.load(json_file)

            # For loop to scrape each product review page
            for url in product_review_urls:
                scraping_review_detail(page, url['asin'], url['url']) # Scrape Review Page, ASIN use to identify the product and cleaner JSON file

        # Close Playwright
        browser.close()
    """
    # Turn JSON file into a list of dictionaries
    list_of_dicts = []
    with open(r'output\amazon_review_data_1.json', 'r', encoding="utf-8") as json_file:
        for line in json_file:
            dict_data = json.loads(line)
            list_of_dicts.append(dict_data)

    with open(r'output\amazon_review_data_2.json', 'w', encoding="utf-8") as json_file:
        json.dump(list_of_dicts, json_file, indent=4, ensure_ascii=False)
        
def loading_page(page, url):

    # Max attempts
    max_attempts = 3

    # For loop to try loading page
    for i in range(max_attempts):
        
        # Page Load
        page.goto(url)
        page.wait_for_load_state()
        time.sleep(random.randint(5, 10)) # Most of the times it triggers captcha, manually solve it while the program is sleeping
        page.click(".a-spacing-medium:has-text('From the United States')") # Click on the text box

        # Check if page is loaded
        if page.wait_for_selector('#nav-logo-sprites'): # Using the Amazon logo as a selector to check if page is loaded

            # Trigger javascript elements to load all page content
            page.keyboard.press('End')
            time.sleep(random.randint(1, 2))
            page.keyboard.press('Home')
            page.wait_for_load_state()
            break

        # If page is not loaded, try again
        else:
            time.sleep(5)
            continue

# Review Page Scrape Function
def scraping_review_detail(page, asin, url):

    # Loading Page
    loading_page(page, url)
    # Maximum number of review pages to scrape
    target_review_page_scraped = 4

    # For loop to scrape each review page
    for i in range(target_review_page_scraped):
    
        # Parse HTML
        soup = BeautifulSoup(page.content(), "lxml")
        
        # Extract Review Page   
        try:
            review_cards = soup.findAll("div", class_="a-section review aok-relative") # CSS selector of each review card in the review from United States section

            # For loop each review card
            for review_card in review_cards:

                # Dict to store the data
                product_review_data = {}

                # Extract the data and store it in the product_review_data dict
                product_review_data["asin"] = asin

                Username = review_card.find("span", class_="a-profile-name").text.strip()
                product_review_data["username"] = Username

                review_title = review_card.find('a', class_='a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold').text.strip()
                product_review_data["title"] = review_title

                review_loc_date = review_card.find('span', class_="a-size-base a-color-secondary review-date").text.strip()
                product_review_data["loc_date"] = review_loc_date
                
                product_purchased = review_card.find('a', class_='a-size-mini a-link-normal a-color-secondary').text.strip()
                product_review_data["purchased"] = product_purchased

                rating = review_card.find("span", class_="a-icon-alt").text.strip()
                product_review_data["rating"] = rating

                Content = review_card.find("span", class_="a-size-base review-text review-text-content").text.strip()
                product_review_data["content"] = Content

                # Store the data in a JSON file
                with open(r'output\amazon_review_data.json', 'a', encoding='utf-8') as json_file:
                    json.dump(product_review_data, json_file, ensure_ascii=False)
                    json_file.write('\n')

        except:
            print("No Review Page")

        try:
            # Click Next Page 
            if soup.find("li", class_="a-last"):
                page.click("a:has-text('Next page')")
            else:
                break
        except:
            print("No Next Page")

if __name__ == "__main__":
    main()
