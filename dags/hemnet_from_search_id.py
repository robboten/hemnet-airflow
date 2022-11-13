import datetime as dt

import pendulum
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import dag,task
from airflow.models import Variable

import logging
log = logging.getLogger(__name__)

#print util
def print_vars(value):
    log.info(value)

def print_date(**context):
    print(context["execution_date"])

#just some default variables to test with
default_params = {"search_id": "925958", "search_name": "Gärdet"}

#initialize the dag
@dag(
    dag_id='Hemnet_from_search_id',
    start_date= pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule_interval=None,
    tags=['Hemnet Scraping'],
    catchup=False,
    params=default_params
)
#main dag function
def hemnet_pt1():

    #get stored variable from airflow by key name
    @task
    def get_vars(var_key):
        params = Variable.get(var_key, deserialize_json=True)
        return params

    #construct url from variables and arguments
    @task
    def get_request_url(text,key,value,**context):
        import urllib.parse
        print_vars(context['logical_date'])

        log.info(text)

        url=text['url']

        print_vars(f"text: {text}")
        print_vars(f"key: {key}")
        print_vars(f"value: {value}")
        print_vars(f"url: {url}")

        params=text['params'] 

        print_vars(f"params: {params}")
        print_vars(f"paramstype: {type(params)}")

        if value=="":
            req_url=url+key+urllib.parse.urlencode(params)
        elif type(params)==str:
            req_url=url+value
        elif type(params)==dict:
            req_url=f"{url}?{urllib.parse.urlencode(params)}&{key}={value}"

        print_vars(req_url)
        return req_url

    #request an url and output response in either text or json
    @task
    def request_url(url,jbool):
        import requests
        headers=Variable.get("hemnet_headers", deserialize_json=True)
        response = requests.request("GET", url=url, headers=headers)
        print_vars(response.text)
        if jbool:
            return response.json()
        else:
            return response.text

    #specialized task to get the search id from json response
    @task
    def get_search_id(response):
        import json
        json_data=json.loads(response)
        search_id=json_data[0]['id']
        return search_id

    #do first series of tasks
    get_search_id(
        request_url(
            get_request_url(
                get_vars("hemnet_request1"),"?",""
            )
        ,False)
    )

#call the whole thing
hemnet_pt1()