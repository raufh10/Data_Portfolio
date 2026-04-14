import json
import csv
import re

# This script converts the JSON data into CSV format
def main():
    # Process product data json file to csv
    process_product_data()
    # Process brand information from product data json file to csv
    process_brand_information()
    # Process technical information from product data json file to csv
    process_technical_information()
    # Process review data json file to csv
    process_review_data()

def process_product_data():
    # Read JSON data
    with open(r"output\amazon_product_data.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Write CSV data
    with open(r"output\amazon_product_data.csv", 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header (column names) based on the JSON keys in the first object
        if data:
            headers = [] # Create a list for the header
            key_header = list(data[0].keys())[:7] # Create a list of the first 7 keys
            headers.extend(key_header) # Add the first 7 keys to the header list
            csv_writer.writerow(headers) # Write the header row

        # Write the data rows
        for product in data:        
            data = []
            # Loop through the keys in the header list
            for key in headers:
                if key == 'rank':
                    ranks = product.get(key).replace('#','') # Remove the # from the rank before adding it to the list
                    data.append(ranks)
                elif key == 'price':
                    price = product.get(key).replace('$','') # Remove the $ from the price before adding it to the list
                    data.append(price)
                elif key == 'offers':
                    if product.get(key):
                        offer_pattern = re.compile(r' offer.*') # Using regex to remove the text before adding it to the list
                        offers = re.sub(offer_pattern, '', product.get(key))
                        data.append(offers)
                    else:
                        offers = 0 # If there are no offers, set the value to 0
                        data.append(offers)
                else:
                    data.append(product.get(key))
            csv_writer.writerow(data)

def process_brand_information():
    # Read JSON data
    with open(r"output\amazon_product_data.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Write CSV data
    with open(r"output\amazon_brand_information.json", 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header (column names) based on the JSON keys in the first object
        if data:
            headers = [] # Create a list for the header
            key_header = list(data[0].keys())[0] # Create a list of the first key
            headers.append(key_header) # Add the first key to the header list
            # Create a list for keys in the brand_information dictionary
            brand_information_key_list = []
            # Loop through the data to get the keys in the brand_information dictionary
            for item in data:
                brand_information = item.get("brand_information")
                try:
                    for key in brand_information:
                        if key not in brand_information_key_list: # If the key is not in the list, add it to the list
                            brand_information_key_list.append(key)
                except:
                    continue
            headers.extend(brand_information_key_list) # Add the keys in the brand_information dictionary to the header list
            csv_writer.writerow(headers) # Write the header row

        # Write the data rows
        for product in data:
            # Create a dictionary for the data
            data_dict = {}
            # Loop through the keys in the header list
            for header in headers:
                
                if header == 'asin': # If the key is asin, add the value to the dictionary
                    data_dict[header] = product.get(header)
                else:
                    # If the brand_information dictionary is empty, set the value to null
                    if product.get("brand_information") == None:
                        data_dict[header] = "null"
                    else:
                        brand_information = product.get("brand_information") # Get the brand_information dictionary
                        header_information = brand_information.get(header) # Get the value of the key in the brand_information dictionary
                        # If the value inside brand_information dictionary is null, set the value to null
                        if header_information == None:
                            data_dict[header] = "null"
                        else:
                            # If the value is a list, join the list and add it to the dictionary
                            if isinstance(header_information, list):
                                data_dict[header] = ", ".join(header_information)
                            else:
                                data_dict[header] = brand_information.get(header) # Add the value to the dictionary
            
            csv_writer.writerow(data_dict.values()) # Write the data row per product item

def process_technical_information():
    # Read JSON data
    with open(r"output\amazon_product_data.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Write CSV data
    with open(r"output\amazon_technical_information.json", 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header (column names) based on the JSON keys in the first object
        if data:
            headers = [] # Create a list for the header
            key_header = list(data[0].keys())[0] # Create a list of the first key
            headers.append(key_header) # Add the first key to the header list
            technical_information_key_list = [] # Create a list for keys in the technical_information dictionary
            for item in data:
                technical_information = item.get("technical_information")
                try:
                    for key in technical_information:
                        if key not in technical_information_key_list: # If the key is not in the list, add it to the list
                            technical_information_key_list.append(key)
                except:
                    continue
            headers.extend(technical_information_key_list) # Add the keys in the technical_information dictionary to the header list
            csv_writer.writerow(headers)

        # Write the data rows
        for product in data:
            data_dict = {}
            # Loop through the keys in the header list
            for header in headers:
                if header == 'asin': # If the key is asin, add the value to the dictionary
                    data_dict[header] = product.get(header)
                else:
                    # If the technical_information dictionary is empty, set the value to null
                    if product.get("technical_information") == None:
                        data_dict[header] = "null"
                    else:
                        technical_information = product.get("technical_information") # Get the technical_information dictionary
                        header_information = technical_information.get(header) # Get the value of the key in the technical_information dictionary
                        # If the value inside technical_information dictionary is null, set the value to null
                        if header_information == None:
                            data_dict[header] = "null"
                        else:
                            # If the value is a list, join the list and add it to the dictionary
                            if isinstance(header_information, list):
                                data_dict[header] = ", ".join(header_information)
                            else:
                                data_dict[header] = technical_information.get(header) # Add the value to the dictionary

            csv_writer.writerow(data_dict.values())

def process_review_data():
    # Read JSON data
    with open(r"output\amazon_review_data.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Write CSV data
    with open(r"output\amazon_review_data.csv", 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header (column names) based on the JSON keys in the first object
        if data:
            headers = [] # Create a list for the header
            key_header = list(data[0].keys())[:5] # Create a list of the first 5 keys
            headers.extend(key_header) # Add the first 5 keys to the header list
            purchase_information_key_list = [] # Create a list for keys in the purchase_information dictionary
            # Loop through the data to get the keys in the purchase_information dictionary
            for item in data:
                purchase_information = item.get("purchase_information")
                try:
                    for key in purchase_information:
                        if key not in purchase_information_key_list: # If the key is not in the list, add it to the list
                            purchase_information_key_list.append(key)
                except:
                    continue
            headers.extend(purchase_information_key_list) # Add the keys in the purchase_information dictionary to the header list
            csv_writer.writerow(headers) # Write the header row

        # Write the data rows
        for product in data:        
            data_dict = {}
            # Loop through the keys in the header list
            for header in headers:
                if header == 'purchase_information': # Check if the key is purchase_information
                    # If header is purchase_information, get the value of the keys in the purchase_information dictionary
                    purchase_information = product.get("purchase_information")
                    header_information = purchase_information.get(header)
                    # If the value inside purchase_information dictionary is null, set the value to null
                    if header_information == None:
                        data_dict[header] = "null"
                    else: # If value is not null, add the value to the dictionary
                        data_dict[header] = header_information
                # If the key is not purchase_information, add the value to the dictionary
                else:
                    data_dict[header] = product.get(header)
            csv_writer.writerow(data_dict.values()) # Write the data row per product item

if __name__ == "__main__":
    main()
