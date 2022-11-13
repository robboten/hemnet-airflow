import json
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests

# Create a folder for all the files

# Parent directory path
parent_dir_path = "./data/areas_of_interest/"

# Current utc date and time
utcnow = datetime.utcnow().strftime("%Y%m%d_%H%M")
dateoftoday = datetime.utcnow().strftime("%Y%m%d")

# Directory path
directory_path = f"{parent_dir_path}{utcnow}/"

# Varible to keep the count of the listings.    
listings_count = 0

listing_json= {
    url:"https://www.hemnet.se/locations/show",
    'params':{'q':'Gärdet, Stockholm'},
    'payload':{},
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
}
    
#use dict to search for listings
url = "https://www.hemnet.se/locations/show"
params= {
    'q':'Gärdet, Stockholm'
}
payload={}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
}


def get_search_id():
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    print(response.text)
    json_data=json.loads(response.text)
    search_id=json_data[0]['id']
    print(search_id)
    get_listing(search_id)

def get_listing(): 
    search_id=925958
    #use dict to search for listings
    url = "https://www.hemnet.se/bostader"
    params= {
        'housing_form_groups':'apartments',
        'location_ids':search_id,
        'item_types':'bostadsratt',
        'rooms_min':2,
        'living_area_min':35,
        'new_construction':'exclude'
    }
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    print(response.url)

    soup = BeautifulSoup(response.content, "html.parser")
    map_results=soup.find(id="results-map")
    initial_data=map_results.attrs["data-initial-data"]
    json_data=json.loads(initial_data)
    print(json_data['search_key'])

    url = "https://www.hemnet.se/bostader/search/"+json_data['search_key']
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    r_json = response.json()
    r_properties = r_json['properties']
     # Store all the listings in that area as a dataframe
    df = pd.json_normalize(
        r_properties,
        max_level=1
    )
    area="Hjorthagen"
    print(f"{area}:\t\t {df.shape}")

    # Enrich the df with info about internal area naming and date  
    df["area"] = area
    df["date"] = dateoftoday

    print(df)
