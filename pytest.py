import json
import requests

# Retrieve the JSON-LD file from the URL
url = "https://ccf-api.hubmapconsortium.org/v1/hubmap/rui_locations.jsonld?key="
response = requests.get(url)
data = response.json()

# List of target strings to filter
target_filters = ['filter_value1', 'filter_value2', 'filter_value3']

# Filter donor entities based on target property
filtered_donors = [entity for entity in data['@graph'] if '@type' in entity and entity['@type'] == 'Donor' and 'rui_location' in entity and 'placement' in entity['rui_location'] and 'target' in entity['rui_location']['placement'] and entity['rui_location']['placement']['target'] in target_filters]

# Filter sample entities based on target property
filtered_samples = [entity for entity in data['@graph'] if '@type' in entity and entity['@type'] == 'Sample' and 'rui_location' in entity and 'placement' in entity['rui_location'] and 'target' in entity['rui_location']['placement'] and entity['rui_location']['placement']['target'] in target_filters]

# Print filtered donor entities
print("Filtered Donor Entities:")
for donor in filtered_donors:
    print("Donor ID:", donor['@id'])
    print("Target:", donor['rui_location']['placement']['target'])
    print("")

# Print filtered sample entities
print("Filtered Sample Entities:")
for sample in filtered_samples:
    print("Sample ID:", sample['@id'])
    print("Target:", sample['rui_location']['placement']['target'])
    print("")
