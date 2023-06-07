import requests
import json
from functions import *

# Define the target IDs
target_starts = ['http://purl.org/ccf/latest/ccf.owl#VHMHeart',
                 'http://purl.org/ccf/latest/ccf.owl#VHFHeart', 
                 'http://purl.org/ccf/latest/ccf.owl#VHMLung', 
                 'http://purl.org/ccf/latest/ccf.owl#VHFLung'
            ]
# Define the URL of the JSON files
dataSources = [
      'assets/kpmp/data/rui_locations.jsonld',
      'assets/sparc/data/rui_locations.jsonld',
      'assets/gtex/data/rui_locations.jsonld',
      'assets/sea-ad/data/rui_locations.jsonld',
      'assets/allen-institute/data/rui_locations.jsonld'
    ]
url_prefix = "https://raw.githubusercontent.com/hubmapconsortium/ccf-ui/main/projects/ccf-eui/src/"

for source in dataSources: 
    url = url_prefix + source
    provider_name = source.split('/')[1]

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        data = json.loads(normalize_rui_location_json(data))
        print(type(data))

        # Find all "samples" lists and remove items that do not match the value of "target"
        donor_count = 0
        for item in data['@graph']:
            if 'samples' in item:
                samples = item['samples']
                for sample in samples:
                    print(sample['rui_location']['placement']['target'])
                    print(donor_count)        
                item['samples'] = remove_samples_without_target(samples, target_starts)
            donor_count = donor_count+1
    
            #remove donor entity from list if they do not have heart or lung samples
            donors = data['@graph']
            data['@graph'] = remove_donors_without_samples(donors)

        # Save the modified JSON to a file
        filename = provider_name + "_heart_and_lung_rui_locations.jsonld"
        with open("eui_data/" + filename, "w") as file:
            json.dump(data, file, indent=4)
