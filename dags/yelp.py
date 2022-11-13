from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
import requests

# dag creation
def url_generator(ti):
    """ 
    generating the yelp url to find the business listings with place and search_query 
    {'place': 'Location | Address | zip code'}
    {'search_query': "Restaurants | Breakfast & Brunch | Coffee & Tea | Delivery | Reservations"}
    """
    place = Variable.get("place")
    search_query = Variable.get("search_query")
    yelp_url = "https://www.yelp.com/search?find_desc={0}&find_loc={1}".format(search_query,place)
    return yelp_url

def get_response(**context):
    """
    validating the url and forwarding the response
    """
    url = context['ti'].xcom_pull(task_ids='url_generator')
    print('url generated: ', url)
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chrome/70.0.3538.77 Safari/537.36'}
    success = False
    
    for retry in range(10):
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code == 200:
            success = True
            break
        else:
            print("Response received: %s. Retrying : %s"%(response.status_code, url))
            success = False
    
    if success == False:
        print("Failed to process the URL: ", url)
        raise ValueError("Failed to process the URL: ", url)
    return response.text

default_args = {
    'owner': 'turbolab', 
    'start_date': datetime(2019, 1, 1), 
    'depends_on_past': False
    }
_yelp_workflow = DAG(
    '_yelp_workflow', 
    catchup=False, 
    schedule_interval=None, 
    default_args=default_args
) # creating a DAG

"""defining a task"""
yelp_url_generator = PythonOperator(
    task_id='url_generator',
    python_callable=url_generator,
    provide_context=True,
    dag=_yelp_workflow
)

response_generator = PythonOperator(
    task_id='response_generator',
    python_callable=get_response,
    provide_context=True,
    dag=_yelp_workflow
)

yelp_url_generator >> response_generator