import json
import pendulum
import requests
from bs4 import BeautifulSoup

from airflow.decorators import dag, task
from airflow.models import Variable


@dag(
    dag_id='Hemnet_ids_shortToLong',
    start_date= pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule_interval=None,
    tags=['Hemnet Scraping'],
    catchup=False
) 
def hemnet_jobs_1():

    @task
    def convert_ids():
        #load list of area ids and the search url from airflow variables
        area_ids=Variable.get("hemnet_area_ids", deserialize_json=True)
        #area_maps_ids=Variable.get("hemnet_area_maps_ids", deserialize_json=True)

        map_keys={}
        url = "https://www.hemnet.se/bostader"
        headers = {"User-Agent": "Mozilla/5.0"}

        for id in area_ids:
            print(area_ids[id]['area_code'])
            #print(id["area_code"])

            area_code = area_ids[id]["area_code"]
            print(area_code)

            # Request HTML to scrape for ids
            params= {
                "housing_form_groups":"apartments",
                "location_ids":area_code,
                "item_types":"bostadsratt",
                "rooms_min":0,
                "living_area_min":0,
                "new_construction":"include"
            } 

            response = requests.request(
                "GET",
                url,
                params=params,
                headers=headers
            )
            #print(response.url)

            soup = BeautifulSoup(response.content, "html.parser")
            map_results=soup.find(id="results-map")

            initial_data=map_results.attrs["data-initial-data"]
            json_data=json.loads(initial_data)

            #print(json_data)

            map_keys[id]=json_data['search_key']

        json_map_keys=json.dumps(map_keys,sort_keys=True, indent=4)
        print(json_map_keys)
        desc="Longer area map codes for hemnet search."
        Variable.set("hemnet_area_maps_ids", json_map_keys, description=desc, serialize_json=False)
        #with open(f"../configs/area_map_ids.json", "w") as file_out:
        #    file_out.write(json_map_keys)

    convert_ids()


hemnet_jobs_1()