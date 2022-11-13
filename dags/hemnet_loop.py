def hemnet_loop(exec_date):
    import pandas as pd
    import requests
    from airflow.models import Variable

    #load list of area ids and the search url from airflow variables
    area_info=Variable.get("hemnet_area_maps_ids", deserialize_json=True)
    params=Variable.get("hemnet_url_map_search", deserialize_json=True)

    # Current date and time for dag run
    utcnow = exec_date.strftime("%Y%m%d_%H%M")
    dateoftoday=exec_date.strftime("%Y%m%d")

    # Directory path and file name (can't move from dags folder atm due to mounting in docker)
    directory_path = "./dags/data/"
    parquet_file_name=f"{utcnow}_all"

    # Varible to keep the count of the listings.    
    listings_count = 0

    #print(type(area_info))

    #make and empty list to store the dataframes for each area
    df_list=list()
    
    headers = params['headers'] #{"User-Agent": "Mozilla/5.0"}
    mapids_url=params['url'] #"https://www.hemnet.se/bostader/search/"

    # Loop thruogh all the areas one by one
    for area,area_code in area_info.items():
        url = mapids_url+area_code

        #make the request
        response = requests.request(
            "GET",
            url,
            headers=headers,
        )

        #print(response.url)

        # Store all the listings in that area as a dataframe
        df = pd.json_normalize(response.json(),
            record_path="properties",
            max_level=1
        )

        # Enrich the df with info about internal area naming and date  
        df["area"] = area
        df["date"] = dateoftoday

        # Update the listings_count
        listings_count += df.shape[0]

        #print shape for each area
        print("{:<20} {:<15}".format(area, str(df.shape)))
        
        #append df to list
        df_list.append(df)

    #merge the dataframes into one
    df_merged=pd.concat(df_list)

    #save the merged dataframe into parquet
    df_merged.to_parquet(f"{directory_path}{parquet_file_name}.parquet", compression=None)
    #df_merged.to_parquet(f"{directory_path}{utcnow}_all.parquet.gzip", compression="gzip")

    #print listing counts before returning
    print(f"\n{listings_count} listings in the areas of interest today!")

    return df_list