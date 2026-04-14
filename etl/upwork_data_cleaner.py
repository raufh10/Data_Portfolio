import re
import json

# Main function
def main():
    # Declare job_list to store all job data
    job_list = []
    # Open json file and read data
    with open(r'output\job_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Loop through each job post
        for item in data:
            post_data = {} # Declare post_data to store each job post data
            # Get job_id
            job_id = item['job_id']
            # Get title
            title = item['title']
            # Get domestic_label
            domestic_label = item['domestic_label']
            domestic_label = domestic_label.replace('\n   \n    ', '')
            # Get description
            description = item['description']
            patterns = [
                r'\t',
                r'\n',
                r'\s+',
            ]
            for pattern in patterns:
                description = re.sub(pattern, ' ', description)
            # Get features
            features_dict = {}
            features = item['features']
            # Loop through each feature and clean data
            for feature in features:
                if 'Project Type' in feature:
                    project_type = feature.replace(' Project Type', '')
                    features_dict['project_type'] = project_type
                if 'hrs/week Hourly' in feature:
                    hours_per_week = feature.replace(' hrs/week Hourly', '')
                    features_dict['hours_per_week'] = hours_per_week
                if 'Duration' in feature:
                    duration = feature.replace(' Duration', '')
                    features_dict['duration'] = duration
                if 'Experience Level' in feature:
                    experience_level = feature.replace(' Experience Level', '')
                    features_dict['experience_level'] = experience_level
                # Get hourly rate
                pattern = r'\$\d+.\d+ Hourly'
                if re.search(pattern, feature):
                    hourly_rate = feature.replace(' Hourly', '').replace('$', '').replace(',', '')
                    hourly_rate = hourly_rate.split(' - ')
                    min_hourly_rate = float(hourly_rate[0])
                    features_dict['min_hourly_rate'] = min_hourly_rate
                    try:
                        max_hourly_rate = float(hourly_rate[1])
                        features_dict['max_hourly_rate'] = max_hourly_rate
                    except:
                        pass
                # Get fixed price
                if 'Fixed-price' in feature:
                    fixed_price = feature.replace(' Fixed-price', '').replace('$', '').replace(',', '')
                    fixed_price = float(fixed_price)
                    features_dict['fixed_price'] = fixed_price
                # Get contract-to-hire or not
                if 'Contract-to-hire' in feature:
                    contract_to_hire = True
                else:
                    contract_to_hire = False
                features_dict['contract_to_hire'] = contract_to_hire
                # Get remote job or not
                if 'Remote Job' in feature:
                    remote_job = True
                else:
                    remote_job = False
                features_dict['remote_job'] = remote_job
            # Store all data to post_data
            post_data = {
                'job_id': job_id,
                'title': title,
                'domestic_label': domestic_label,
                'description': description,
                'features': features_dict
            }
            # Append post_data to job_list
            job_list.append(post_data)
            
    # Write job_list to json file
    with open(r'output\job_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(job_list, json_file, indent=4)

if __name__ == '__main__':
    main()