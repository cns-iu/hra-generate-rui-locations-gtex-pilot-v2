import json
import os
import subprocess

# Run first script
subprocess.run(['python', 'get_hubmap_rui_locations.py'])

# Run second script
subprocess.run(['python', 'get_other_asset_rui_locations.py'])

###update rui_location.jsonld###

# Path to the "eui_data" folder
folder_path = "eui_data"

# List to store the graph items
graph_items = []

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Check if the file is a JSON-LD file
    if filename.endswith(".jsonld"):
        with open(file_path, "r") as file:
            data = json.load(file)
            if "@graph" in data:
                # Append the graph items to the list
                graph_items.extend(data["@graph"])

# Create the final JSON-LD data with the combined graph items
final_data = {
            "@context": {
                "@base": "http://purl.org/ccf/latest/ccf-entity.owl#",
                "@vocab": "http://purl.org/ccf/latest/ccf-entity.owl#",
                "ccf": "http://purl.org/ccf/latest/ccf.owl#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "label": "rdfs:label",
                "description": "rdfs:comment",
                "link": {
                    "@id": "rdfs:seeAlso",
                    "@type": "@id"
                },
                "samples": {
                    "@reverse": "has_donor"
                },
                "sections": {
                    "@id": "has_tissue_section",
                    "@type": "@id"
                },
                "datasets": {
                    "@id": "has_dataset",
                    "@type": "@id"
                },
                "rui_location": {
                    "@id": "has_spatial_entity",
                    "@type": "@id"
                },
                "ontologyTerms": {
                    "@id": "has_ontology_term",
                    "@type": "@id"
                },
                "cellTypeTerms": {
                    "@id": "has_cell_type_term",
                    "@type": "@id"
                },
                "thumbnail": {
                    "@id": "has_thumbnail"
                }
            },
            "@graph": graph_items
        }

# Write the final data to the new JSON-LD file
output_file = "rui_locations.jsonld"
with open(output_file, "w") as file:
    json.dump(final_data, file, indent=2)

print(f"New JSON-LD file '{output_file}' created successfully.")
