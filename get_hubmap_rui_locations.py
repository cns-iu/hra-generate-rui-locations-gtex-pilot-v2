import json
import requests
import os
from functions import *

#load data
file_url = r"https://ccf-api.hubmapconsortium.org/v1/hubmap/rui_locations.jsonld?key="
file_path = r"downloaded_data/entity_api_call_rui_locations.jsonld"
target_starts = ['http://purl.org/ccf/latest/ccf.owl#VHMHeart','http://purl.org/ccf/latest/ccf.owl#VHFHeart', 'http://purl.org/ccf/latest/ccf.owl#VHMLung', 'http://purl.org/ccf/latest/ccf.owl#VHFLung']
data = open_json_file(file_path, file_url)

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

# Save the modified data to a new JSON-LD file
with open('eui_data/'+'hubmap_rui_locations.jsonld', 'w') as file:
    json.dump(data, file, indent=2)
    

