import re
import json
from datetime import datetime

def main():
    # Declare a list to store the splitters for each function
    brand_splitters = []
    technical_splitters = []
    review_splitters = []
    
    # Call the functions to clean the brand, technical and review data 
    brand_splitter_pattern(brand_splitters) # This function is used to find the splitters in the brand data
    technical_splitter_pattern(technical_splitters) # This function is used to find the splitters in the technical data

    # Declare a dict to store the data after cleaning
    brand_dict = {}
    technical_dict = {}

    brand_information_clean(brand_splitters, brand_dict) # This function is used to clean the brand data
    technical_information_clean(technical_splitters, technical_dict) # This function is used to clean the technical data
    storing_data(brand_dict, technical_dict) # This function is used to store the data in a JSON file

    review_splitter_pattern(review_splitters) # This function is used to find the splitters in the review data
    review_data_clean(review_splitters) # This function is used to clean the review data

def brand_splitter_pattern(splitters):
    # Open the JSON file and load the data
    with open(r'output\amazon_product_data_2.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Declare a list to store the categories
        category_list = []
        # Loop through the data items
        for item in data:
            if item["brand_information"] == None: # If there is no brand information continue to the next item
                continue
            brand_information = item["brand_information"] # Get the brand information
            brand_information = brand_information.replace("See more", "") # Remove the 'See more' from the brand information
            brand_information = brand_information.replace("  ", " ").strip() # Remove the double spaces from the brand information
            # Declare the pattern to find the categories in this instance Word behind a : and the first letter is capitalized
            information_category_pattern = r'[A-Z][a-zA-Z]*:'
            categories = re.findall(information_category_pattern, brand_information) # Find the categories
            for category in categories:
                category_list.append(category) # Add the categories to the list
        category_set = set(category_list) # Remove the duplicates
        # Print the categories to the console and manually check if indeed these are the categories
        print(category_set)
        # Declare a list to store the splitters
        splitter_list = [
            'Brand:',
            'Special Feature:',
            'Color:',
            'Number of Buttons:',
            'Recommended Uses For Product:',
            'Hand Orientation:',
            'Material:',
            'Connectivity Technology:',
            'Movement Detection Technology:',
        ]
        for item in splitter_list:
            splitters.append(item) # Add the splitters to the review_splitters

def technical_splitter_pattern(splitters):
    # Open the JSON file and load the data
    with open(r'output\amazon_product_data_2.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Declare a list to store the categories
        category_list = []
        # Loop through the data items
        for item in data:
            if item["technical_information"] == None: # If there is no technical information continue to the next item
                continue
            technical_information = item["technical_information"] # Get the technical information
            technical_information = re.sub(r'\n', ' ', technical_information) # Remove the new lines from the technical information
            technical_information = re.sub(r'\s+', ' ', technical_information) # Remove the double spaces from the technical information
            # Declare the pattern to find the categories in this instance Word behind a , and the first letter is capitalized and word at the start of the string and the first letter is capitalized
            information_pattern_list = [
                r', [A-Z][a-zA-Z]*\s+',
                r'^[A-Z][a-zA-Z]*\s+',
            ]
            # Loop through the patterns
            for information_pattern in information_pattern_list:
                information_category_pattern = information_pattern # Declare the pattern to find the categories
                categories = re.findall(information_category_pattern, technical_information) # Find the categories
                for category in categories:
                    category_list.append(category) # Add the categories to the list
        category_set = set(category_list) # Remove the duplicates
        # Print the categories to the console and manually check if indeed these are the categories
        print(category_set)
        # Declare a list to store the splitters
        splitter_list = [
            'ASIN',
            'Whats in the box',
            'Package Dimensions',
            'Date First Available',
            'Other display features',
            'Number of USB 2.0 Ports',
            'Number of Processors',
            'Wireless Type',
            'Product Dimensions',
            'Brand',
            'Average Battery Life (in hours)',
            'Standing screen display size',
            'Package Dimensions',
            'Hardware Platform',
            'OS',
            'Operating System',
            'Series',
            'Language',
            'Connectivity technologies',
            'Is Discontinued By Manufacturer',
            'Batteries',
            'Special features',
            'Country of Origin',
            'Best Sellers Rank',
            'Manufacturer',
            'Power Source',
            'Department',
            'Voltage',
            'Item Dimensions',
            'Item model number',
            'Item Weight',
            'Color',
            'Customer Reviews',
        ]
        for item in splitter_list:
            splitters.append(item) # Add the splitters to the review_splitters

def brand_information_clean(splitters, brand_dict):
    # Open the JSON file and load the data
    with open(r'output\amazon_product_data_2.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Loop through the data items
        for item in data:
            # If there is no brand information continue to the next item
            if item["brand_information"] == None:
                continue
            # Declare a dictionary to store the information
            brand_information_dict = {}
            # Get the ASIN
            asin = item["asin"]
            # Get the brand information and clean it from the 'See more' and double spaces
            brand_information = item["brand_information"]
            brand_information = brand_information.replace("See more", "")
            brand_information = brand_information.replace("  ", " ").strip()
            # Loop through the splitters to add a new line before the splitter
            for splitter in splitters:
                splitter_pattern = f', {splitter}'
                replacement = f'\n{splitter}'
                try:
                    brand_information = brand_information.replace(splitter_pattern, replacement)
                except:
                    continue
            # Split the brand information by new line
            brand_information = brand_information.split('\n')
            # Loop through the brand information items and split them by : to make a key and value
            for information in brand_information:
                if ':' in information:
                    print (information)
                    information = information.split(':')
                    information_key = information[0]
                    information_values = information[1]
                    if ', ' in information_values:
                        information_values = information_values.split(', ')
                    # Add the key and value to the dictionary
                    brand_information_dict[information_key] = information_values

            # Store the information in the dictionary
            brand_dict[asin] = brand_information_dict

def technical_information_clean(splitters, technical_dict):
    # Open the JSON file and load the data
    with open(r'output\amazon_product_data_2.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Loop through the data items
        for item in data:
            if item["technical_information"] == None:
                continue
            # Declare a dictionary to store the information
            technical_information_dict = {}
            # Get the ASIN
            asin = item["asin"]
            # Get the technical information and clean it from the new lines and double spaces
            technical_information = item["technical_information"]
            technical_information = re.sub(r'\n', ' ', technical_information)
            technical_information = re.sub(r'\s+', ' ', technical_information)
            technical_information = re.sub('Brand', 'Tech Brand', technical_information)
            # Loop through the splitters to add a new line before the splitter
            for splitter in splitters:
                # Declare the patterns to find the splitters in the technical information
                splitter_patter_start_sentence = f'{splitter} '
                replacement_start_sentence = f'{splitter}: '
                splitter_pattern_mid_sentence = f', {splitter}'
                replacement_mid_sentence = f'\n{splitter} '
                # Replace the splitters with the new line and splitter
                technical_information = technical_information.replace(splitter_patter_start_sentence, replacement_start_sentence)
                technical_information = technical_information.replace(splitter_pattern_mid_sentence, replacement_mid_sentence)        
            # Handle the Average Battery Life (in hours)
            technical_information = technical_information.replace('Average Battery Life (in hours)', 'Average Battery Life (in hours):')
            technical_information = technical_information.replace(', Average Battery Life (in hours)', '\nAverage Battery Life (in hours): 120 Hours')
            # Split the technical information by new line
            technical_information = technical_information.split('\n')
            # Loop through the technical information items and split them by : to make a key and value
            for information in technical_information:
                if ': :' in information:
                    information = information.replace(': :', ':') # If there are two : after each other remove one
                # Split the information by : then make the first part the key and the second part the value
                information = information.split(':')
                information_key = information[0].strip()
                information_values = information[1].strip()
                # If the value contains 'and Xbox. USB port required.' replace it with 'Xbox (USB port required)'
                if 'and Xbox. USB port required.' in information_values:
                    information_values = information_values.replace('and Xbox. USB port required.', 'Xbox (USB port required)')
                # If there is a comma and a space in the value
                if ', ' in information_values:
                    if information_key == 'Date First Available': # If the key is Date First Available continue to the next item
                        continue
                    elif information_key == 'Manufacturer': # If the key is Manufacturer continue to the next item
                        continue
                    else:
                        information_values = information_values.split(', ') # Split the value by comma and space
                # Add the key and value to the dictionary
                technical_information_dict[information_key] = information_values
            # Store the information in the dictionary
            technical_dict[asin] = technical_information_dict

def storing_data(brand_dict, technical_dict):
    # Open the JSON file and load the data
    with open(r'output\amazon_product_data_2.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Declare a list to store selected items
        selected_items = []
        # Loop through the data items
        for item in data:
            asin = item.get('asin') # Get the asin to use as a key to get the information
            offers_text = item.get('offers') # Get the offers text
            if offers_text != None: # If there is offers text
                offers_pattern = r'\d+ offer.*\$'
                offers = re.sub(offers_pattern, '', offers_text) # Remove the offers text from the offers
            else:
                offers = None
            selected_item = {'asin':item.get('asin'),
                            'title':item.get('title'),
                            'rank':int(item.get('rank').replace('#', '')),
                            'price':float(item.get('price').replace('$', '')),
                            'rating_volume':int(item.get('rating_volume').replace(',', '')),
                            'offers':offers,
                            'offers_bool':item.get('offers_bool'),
                            'rating':float(item.get('rating')),
                            'brand_information':brand_dict.get(asin), # Get the brand information from the brand_dict using asin as a key
                            'technical_information':technical_dict.get(asin) # Get the technical information from the technical_dict using asin as a key
                            }
            selected_items.append(selected_item) # Add the selected item to the list

        # Write the merged data to a new JSON file
        with open(r'output\amazon_product_data_3.json', 'w', encoding='utf-8') as merged_file:
            json.dump(selected_items, merged_file, ensure_ascii=False, indent=4)

def review_splitter_pattern(splitters):
    # Open the JSON file and load the data
    with open(r'output\amazon_review_data_1.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Declare a list to store the categories
        category_list = []
        # Loop through the data items
        for item in data:
            purchase_information = item["purchased"] # Get the purchase information
            information_category_pattern = r'[A-Z][a-zA-Z]*:' # Declare the pattern to find the categories in this instance Word behind a : and the first letter is capitalized
            categories = re.findall(information_category_pattern, purchase_information) # Find the categories
            for category in categories:
                category_list.append(category) # Add the categories to the list
        # Remove the categories that have more than one capital letter
        category_list = [item for item in category_list if sum(1 for char in item if char.isupper()) <= 1]
        # Remove the duplicates
        category_set = set(category_list)
        # Print the categories to the console and manually check if indeed these are the categories
        print(category_set)
        # Declare a list to store the splitters
        splitter_list = [
            'Style:',
            'Size:',
            'Pattern Name:',
            'Color:',
        ]
        for item in splitter_list:
            splitters.append(item) # Add the splitters to the review_splitters

def review_data_clean(splitters):
    # Open the JSON file and load the data
    with open(r'output\amazon_review_data_1.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Declare a dictionary to store the information
        information_dict = {}
        # Loop through the data items
        for item in data:
            # Get the ASIN
            asin = item["asin"]
            # Get the title
            title = item["title"]
            title_pattern = r'\d\.\d out of \d stars\n'
            title = re.sub(title_pattern, '', title)
            # Get the location and date variable
            loc_date = item["loc_date"]
            # Get the location
            loc_date = loc_date.split(' on ') # Split the location and date
            location = loc_date[0].replace('Reviewed in the ', '') # Remove the 'Reviewed in the ' from the location
            # Get the date
            orignal_date = loc_date[1]
            input_format = "%B %d, %Y" # Declare the input format
            output_format = "%Y-%m-%d" # Declare the output format
            date = datetime.strptime(orignal_date, input_format).strftime(output_format) # Convert the date to the output format using lib datetime
            # Get the purchase information
            purchase_information_dict = {}
            purchase_information = item["purchased"]
            # Loop through the splitters to add a new line before the splitter
            for splitter in splitters:
                splitter_pattern = f'{splitter}'
                replacement = f'\n{splitter}'
                if splitter in purchase_information:
                    purchase_information = purchase_information.replace(splitter_pattern, replacement).strip()
            # Split the purchase information by new line
            purchase_information = purchase_information.split('\n')
            # Loop through the purchase information items
            for information in purchase_information:
                information = information.split(':') # Split the information by :
                information_key = information[0].strip() # Make the first part into the key
                information_values = information[1].strip() # Make the second part into the value
                if ', ' in information_values: # If there is a comma and a space in the value
                    information_values = information_values.split(', ') # Split the value by comma and space
                purchase_information_dict[information_key] = information_values # Add the key and value to the dictionary

            # Store the information in the dictionary
            information_dict["asin"] = {"asin":asin, "title":title, "location":location, "date":date, "purchase_information":purchase_information_dict}

        # Declare a list to store selected items
        selected_items = []
        # Loop through the data items
        for item in data:
            asin = item.get('asin') # Get the asin to use as a key to get the information
            selected_item = {'asin':asin,
                     'username':item.get('username'),
                     'title':information_dict.get(asin, {}).get("title", None), # Get the title from the information_dict using asin as a key
                     'location':information_dict.get(asin, {}).get("location", None), # Get the location from the information_dict using asin as a key
                     'date':information_dict.get(asin, {}).get("date", None), # Get the date from the information_dict using asin as a key
                     'purchase_information':information_dict.get(asin, {}).get("purchase_information", None), # Get the purchase information from the information_dict using asin as a key
                     'rating':item.get('rating'),
                     'content':item.get('content'),
                     }
            selected_items.append(selected_item) # Add the selected item to the list
        
        # Store the data in a JSON file
        with open(r'output\amazon_review_data_2.json', 'w', encoding='utf-8') as json_file:
            json.dump(selected_items, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()