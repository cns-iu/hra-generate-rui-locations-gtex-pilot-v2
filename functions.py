import json
import requests
import os

#check if JSONLD has been downloaded from HuBMAP ccf-api
def check_file(url, file_path):
    if os.path.isfile(file_path):
        print(f"The file '{file_path}' already exists.")
    else:
        print(f"The file '{file_path}' does not exist. Downloading from {url}...")
        try:
            response = requests.get(url)
            data = response.json()
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            print("File downloaded successfully.")
        except Exception as e:
            print(f"Error occurred while downloading the file: {e}")

#open rui_locations.jsonld
def open_json_file(file_path, file_url):
    #check if file has been downloaded
    check_file(file_url, file_path)
    #load data
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def remove_samples_without_target(samples, target_starts_list):
    return [sample for sample in samples if
            any(sample['rui_location']['placement']['target'].startswith(start) for start in target_starts_list)]

def remove_donors_without_samples(donors):
    new_list = []
    for donor in donors:
        if donor['samples']==[]:
            print("Donor ID "+donor['@id']+" has been removed - "+str(len(donor['samples']))+" samples found")
        else:
            new_list.append(donor)
    return(new_list)

CONTEXT = {
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
}

def normalize_rui_location_json(data):
    json_structure = { "@context": CONTEXT, "@graph": [] }
    if isinstance(data, list):
        json_structure["@graph"] = data
    elif isinstance(data, dict):
        if "@graph" in data:
            json_structure = data
        elif "@type" in data:
            json_structure["@graph"] = [ data ]
    else:
        raise ValueError("Invalid data format")

    return json.dumps(json_structure, indent=2)
