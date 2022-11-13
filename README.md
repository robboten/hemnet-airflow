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