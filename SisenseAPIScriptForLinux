
# This code will build elasticube through API

import requests
import urllib3
from urllib.request import urlretrieve

def buildEcube(ecube, usern, passw):
   
    url = 'http://10.231.32.247:30845/api/v1/authentication/login' # URL to generate API token 
    header = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"} # Headers to be used with URL in POST request 
    myobj = {'username': usern, 'password': passw} # Data to be passed with URL in POST request 
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # To disable warnings in output 
    response = requests.post(url ,headers = header, data = myobj, verify = False) # POST request to generate API Token 
    my_json = response.json() # Converting output to json format 
    token = my_json['access_token'] # Retrieving the value of access_token from json output. This is the Token, which will be used for further actions.
    
    uuidurl = 'http://10.231.32.247:30845/api/v2/datamodels/schema?title='+ ecube +'' # API to get datamodel schema details
    uuidheader = {'Authorization': 'Bearer ' +token, 'Content-Type': 'application/json'}
    uuidresponse = requests.get(uuidurl, headers = uuidheader)
    response = uuidresponse.json()
    uuid = (response["oid"]) # Fetching datamodelId to use in build API call
    
    url = "http://10.231.32.247:30845/api/v2/builds"   
    withHeader = {'Authorization': 'Bearer ' +token, 'Content-Type': 'application/json'} 
    mydata = '{ "datamodelId": "' + uuid + '", "buildType": "full", "rowLimit": 100}' 
    response = requests.post(url, headers = withHeader, data = mydata)
    
    if response.status_code == 201:
        print('Build started successfully!')
    else:
        print('Build failed with status code: ' + response.status_code)
        
    
if __name__ == "__main__":
    
    buildEcube('Sample ECommerce', 'admin@ge.com', 'Sisense@GE123') # Calling function with eCube name, username and password parameters to build eCube.
    
    
    # NOTES:
    
    # HTTP Status Codes
    # =================
    # 200/201   Success
    # 400	invalid elasticube or server
    # 403	forbidden
    
    # Build Types
    # ===========
    # None - Updates the ElastiCube server with the ElastiCube schema, without building.
    # Full - Rebuilds the ElastiCube from scratch.
    # Delta - Rebuilds from scratch tables that have changed in the ElastiCube schema.
    # FullUpdateExisting - Rebuilds the ElastiCube and accumulates data for tables marked as accumulative. This mode should only be used for accumulative builds.
    
 
