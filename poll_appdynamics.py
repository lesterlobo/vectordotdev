import getopt
import json
import sys
import requests
import time
from datetime import datetime, timedelta
import csv


def usage():
    print(__doc__)

def use_oauth_token(token, api_endpoint):
    """Makes a request to an API using an OAuth token."""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


def retrieve_token(client_id, client_secret, controller_url):
    payload = 'grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    tokenResponse = requests.post(controller_url + "/controller/api/oauth/access_token", data=payload)

    token = ''
    if tokenResponse.status_code == 200:
        token = json.loads(tokenResponse.content.decode('utf-8'))['access_token']
        return token
    else:
        raise Exception(f"API request failed with status code {tokenResponse.status_code}")
    

def get_metric(token, controller_url, applicationName, metricPath):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json" 
    }
    metricResponse = requests.get(controller_url + "/controller/rest/applications/" + applicationName + "/metric-data?metric-path=" + metricPath + "&time-range-type=BEFORE_NOW&duration-in-mins=60&output=JSON", headers=headers)
   
    if (metricResponse.ok):
        metric = json.loads(metricResponse.content.decode('utf-8'))
        print(metric)
        return metric
    else:
        raise Exception(f"API request failed with status code {metricResponse.status_code}")
    


def main(argv):
    controller_url = ''
    client_id = ''
    client_secret = ""

    # retrieve api token
    token = retrieve_token(client_id, client_secret, controller_url)

    # # retrieve Metric for Application
    
    get_metric(token, controller_url, "MicroStrategyPBM_DEV", "Overall Application Performance|Calls per Minute")
    get_metric(token, controller_url, "MicroStrategyPBM_DEV", "Overall Application Performance|Average Response Time (ms)")
    get_metric(token, controller_url, "MicroStrategyPBM_DEV", "Overall Application Performance|Errors per Minute")

    
if __name__ == "__main__":
    main(sys.argv[1:])
