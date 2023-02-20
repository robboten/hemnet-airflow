# Hemnet Airflow

Hemnet Airflow is an Apache Airflow pipeline that automates the process of collecting, cleaning, transforming, and analyzing real estate data from Hemnet, a popular real estate website in Sweden.

This pipeline is built using Python and Apache Airflow, a popular open-source platform for creating, scheduling, and monitoring workflows. It uses a variety of tools and techniques, including web scraping, data cleaning, data transformation, and data analysis to produce insights on the real estate market in Sweden.

## Getting Started

To get started with this project, you will need to have Apache Airflow installed on your machine. You can download and install Apache Airflow from the official [Airflow website](https://airflow.apache.org/docs/apache-airflow/stable/start.html).

Once you have Apache Airflow installed, you can clone this repository to your local machine using the following command:

git clone https://github.com/robboten/hemnet-airflow.git


After cloning the repository, you will need to install the required dependencies. You can do this by running the following command:


pip install -r requirements.txt



You will also need to set up a PostgreSQL database to store the collected data. You can do this by following the instructions in the `hemnet-airflow/dags/setup_db.sql` file.

## Running the Pipeline

To run the Hemnet Airflow pipeline, you will first need to start the Airflow web server and scheduler. You can do this by running the following command:

airflow webserver --port 8080

airflow scheduler


Once the web server and scheduler are running, you can navigate to the Airflow web interface at `http://localhost:8080/` to view and manage the pipeline.

To run the pipeline, you can trigger the `hemnet_dag` DAG from the Airflow web interface. This will start the pipeline, which includes the following tasks:

1. `collect_hemnet_data`: This task collects real estate data from Hemnet using web scraping techniques and stores it in a PostgreSQL database.
2. `clean_hemnet_data`: This task cleans and pre-processes the collected data to remove duplicates and invalid records.
3. `transform_hemnet_data`: This task transforms the cleaned data into a format suitable for analysis, including feature engineering and data aggregation.
4. `analyze_hemnet_data`: This task analyzes the transformed data to produce insights on the real estate market in Sweden.

## Configuring the Pipeline

The Hemnet Airflow pipeline can be configured using the `hemnet-airflow/config.py` file. This file contains a variety of configuration options, including the location of the PostgreSQL database, the target URL for web scraping, and the output format for analysis.

## Data Output

The Hemnet Airflow pipeline produces several output files, including:

1. `hemnet_data.csv`: This file contains the raw real estate data collected from Hemnet.
2. `hemnet_cleaned.csv`: This file contains the cleaned real estate data after pre-processing.
3. `hemnet_transformed.csv`: This file contains the transformed real estate data after feature engineering and data aggregation.
4. `hemnet_insights.txt`: This file contains insights on the real estate market in Sweden, including top locations, property types, and average prices.

## Contributing

Contributions to this project are welcome. If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. 
































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



