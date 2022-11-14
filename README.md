# airflow
for macOS to test memory limits. If not at least 4GB is available it will fail  
`docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'`


make a new project folder and create the following dirs (if those does not exist after git pull)  
```
./dags
./data
./plugins
./logs
```
   
`mkdir -p ./dags ./logs ./plugins ./data`  

for linux also run  
`echo -e "AIRFLOW_UID=$(id -u)" > .env`

lastly run  
`docker-compose up -d`

if it doesn't run.. 
run to initialize databases and more (unsure about this one)    
`docker-compose up airflow-init`

When Airflow is running on localhost/8080 open the dag list and activate the dags with tags Hemnet Scraping.     
Edit the area_codes.json as suited and run the Hemnet_init dag to initialize all variables.    
Then run the Hemnet_from_map_id (or wait for schedule to run)    