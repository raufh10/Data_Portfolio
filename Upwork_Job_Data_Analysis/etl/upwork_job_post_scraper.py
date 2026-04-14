from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import json
import time
import random

# Main Function
def main():

    # Playwright sequence
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Using headless=False because most of the times it triggers captcha, manually solve it while the program is running also it is easier to debug
        context = browser.new_context()
        page = context.new_page()

        # Upwork Job Search Starting URL, needed to simulate a real user (could be skipped with a captcha solver and a proxy)
        starting_url = 'https://www.upwork.com/nx/jobs/search/?nbs=1&q=data%20analyst&per_page=50'
        page.goto(starting_url)

        # Scraping the job data
        url = 'https://www.upwork.com/nx/jobs/search/?q=Data%20analyst&sort=recency&category2_uid=531770282580668420&subcategory2_uid=531770282593251330&per_page=50'
        loading_page(page, url)
        scraping_page(page)
        
        # Turn JSON file into a list of dictionaries
        list_of_dicts = []
        with open(r'output\skill_categories.json', 'r') as file:
            for line in file:
                dict_data = json.loads(line)
                list_of_dicts.append(dict_data)

        with open(r'output\skill_categories.json', 'w') as file:
            json.dump(list_of_dicts, file, indent=4)

        # Turn JSON file into a list of dictionaries
        list_of_dicts = []
        with open(r'output\job_data.json', 'r') as file:
            for line in file:
                dict_data = json.loads(line)
                list_of_dicts.append(dict_data)

        with open(r'output\job_data.json', 'w') as file:
            json.dump(list_of_dicts, file, indent=4)
        
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
        # Check if page is loaded
        if page.wait_for_selector('.nav-logo'): # Using the Logo as a selector to check if page is loaded
            # Trigger javascript elements to load all page content
            for i in range(20):
                page.keyboard.press('PageDown')
                time.sleep(0.5)
            page.keyboard.press('End')
            page.keyboard.press('Home')
            page.wait_for_load_state()
            break
        # If page is not loaded, try again
        else:
            time.sleep(1)
            continue

def scraping_page(page):
    
    while True:
        # Parse HTML
        soup = BeautifulSoup(page.content(), "lxml")
        
        # Get skill categories
        scraping_skill_categories(soup)
        
        # Get job data
        for i in range(50):
            # Click the job card using playwright
            job_card = page.locator(f'div.up-job-list section:nth-child({i+1})')
            job_card.click()
            time.sleep(random.randint(4, 6))
            page.wait_for_load_state()

            # Extract job data
            scraping_job_data(page)

            # Go back to the previous page
            page.go_back()
            page.wait_for_load_state()
            time.sleep(random.randint(2, 4))
        
        # Next page Check
        pages_tag = soup.findAll('li', {'class':'pagination-link'})
        next_page_tag = pages_tag[-1].find('button')
        next_page_flag = next_page_tag.get('disabled')
        if next_page_flag == 'disabled':
            break

        # Next page Click
        try:
        # Wait for the "Next" button to be available
            page.wait_for_selector('ul.up-pagination li:nth-child(9)')
            # Click the 9th <li> element which contains the "Next" button
            li_element = page.locator('ul.up-pagination li:nth-child(9)')
            li_element.click()
        except Exception as e:
            print(f"An error occurred: {e}")

        # Trigger javascript elements to load all page content
        for i in range(20):
            page.keyboard.press('PageDown')
            time.sleep(0.5)
        page.keyboard.press('End')
        page.keyboard.press('Home')
        time.sleep(3)
        page.wait_for_load_state()

def scraping_skill_categories(soup):
    # Get Skill Categories
    post_container = soup.find('div', {'class':'up-job-list'})
    posts = post_container.findAll('section', {'class':'up-card-section up-card-list-section up-card-hover'})
    # Loop through each post
    for post in posts:
        skill_categories = {}

        # Get Job ID
        title_link_tag = post.find('a', {'class':'up-n-link'})
        title_url = title_link_tag.get('href')
        pattern = r'~(\d+)'
        job_id = re.search(pattern, title_url).group(0)

        # Get Job Skills List
        #skills_tag = post.find('div', {'class':'up-skill-wrapper'})
        skills_tag = post.findAll('a', {'data-test':'attr-item'})
        skills = []
        for skill in skills_tag:
            skills.append(skill.text)

        # Store Job Skills List in skill_categories
        skill_categories[job_id] = skills

        # Store the data in a JSON file
        with open(r'output\skill_categories.json', 'a', encoding='utf-8') as json_file:
            json.dump(skill_categories, json_file, ensure_ascii=False)
            json_file.write('\n')

def scraping_job_data(page):
    # Initialize job_data_dict
    job_data_dict = {}

    # Parse HTML
    soup = BeautifulSoup(page.content(), "lxml")

    # Get Job ID
    title_url = page.url
    pattern = r'~(\d+)'
    job_id = re.search(pattern, title_url).group(0)
    # Get Job Title, Domestic Label, and Description
    title = soup.find('h1').text.strip()
    domestic_label = soup.find('div', {'data-test':'location-restriction-label'}).text.strip()
    description = soup.find('div', {'class':'job-description break mb-0'}).text.strip()
    # Get Job Features
    features = []
    job_features_tag = soup.find('ul', {'data-test':'job-features'})
    job_features = job_features_tag.findAll('li')
    for job_feature in job_features:
        job_feature = job_feature.text.strip()
        job_feature = re.sub(r'\s+', ' ', job_feature)
        features.append(job_feature)
    # Store Job Data in job_data_dict
    job_data_dict['job_id'] = job_id
    job_data_dict['title'] = title
    job_data_dict['domestic_label'] = domestic_label
    job_data_dict['description'] = description
    job_data_dict['features'] = features

    # Store the data in a JSON file
    with open(r'output\job_data.json', 'a', encoding='utf-8') as json_file:
        json.dump(job_data_dict, json_file, ensure_ascii=False)
        json_file.write('\n')

if __name__ == "__main__":
    main()