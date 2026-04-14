import re
import json

# Main function
def main():
    # Declare job_list to store all job data
    job_list = []
    # Open json file and read data
    with open(r'output\job_data.json', 'r', encoding='utf-8') as job_json, \
         open(r'output\skill_categories.json', 'r', encoding='utf-8') as skills_json:
    
        job_data = json.load(job_json)
        skills_data = json.load(skills_json)

        # Loop through each job post
        for index, (post, skills) in enumerate(zip(job_data, skills_data)):
            post_data = {} # Declare post_data to store each job post data
            # Get job_id
            job_id = post['job_id']
            skills_id = list(skills.keys())[0]
            if job_id == skills_id:
                post_data['job_id'] = job_id
            else:
                print(f'Job id {index} not found in skills data')
                continue
            # Get title
            title = post['title']
            post_data['title'] = title
            # Get domestic_label
            domestic_label = post['domestic_label']
            post_data['domestic_label'] = domestic_label
            # Get description
            description = post['description']
            post_data['description'] = description
            # Get features
            features_type = [
                'project_type', 'hours_per_week', 'duration',
                'experience_level', 'min_hourly_rate', 'max_hourly_rate',
                'fixed_price', 'contract_to_hire', 'remote_job'
            ]
            for feature in features_type:
                try:
                    post_data[feature] = post[feature]
                except:
                    post_data[feature] = None
            
            # Get skills
            skills_list = skills[job_id]
            post_data['skills'] = skills_list

            # Append post_data to job_list
            job_list.append(post_data)
            
    # Write job_list to json file
    with open(r'output\job_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(job_list, json_file, indent=4)

if __name__ == '__main__':
    main()