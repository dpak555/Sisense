# This code will build elasticube through API.
# This is for Linux.
# API v2.0 has been used.

import requests
import urllib3


def buildEcube(ecube, usern, passw):

    url = 'http://10.231.32.247:30845/api/v1/authentication/login'  # URL to generate API token
    header = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}  # Headers to be used with URL in POST request
    myobj = {'username': usern, 'password': passw}  # Data to be passed with URL in POST request
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # To disable warnings in output
    response = requests.post(url, headers=header, data=myobj, verify=False)  # POST request to generate API Token
    my_json = response.json()  # Converting output to json format
    token = my_json['access_token']  # Retrieving the value of access_token from json output. This is the Token, which will be used for further actions.

    # ecubeBuildUrl = 'http://10.231.32.247:30845/api/elasticubes/localhost/' + ecube + '/startBuild?type=Full' # URL to build ecube with build type
    # withHeader = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + (token)} # Headers to be used with URL in POST request
    # ecubebuildResponse = requests.post(ecubeBuildUrl, headers=withHeader, verify=False) # POST request to build elasticube
    # print(ecubebuildResponse.text) # Printing the response code

    uuidurl = 'http://10.231.32.247:30845/api/v2/datamodels/schema?title=' + ecube + ''
    uuidheader = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    uuidresponse = requests.get(uuidurl, headers=uuidheader)
    res = uuidresponse.json()
    uuid = (res["oid"])

    url = "http://10.231.32.247:30845/api/v2/builds"
    withHeader = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    mydata = '{ "datamodelId": "' + uuid + '", "buildType": "full", "rowLimit": 100}'
    response = requests.post(url, headers=withHeader, data=mydata)
    if response.status_code == 201 or 200:
        print('Build started successfully!')
    else:
        print('Build failed with status code: ' + response.status_code)


if __name__ == "__main__":
    buildEcube('Sample ECommerce', 'admin@ge.com', 'Sisense@GE123')  # Calling function with eCube name, username and password parameters to build eCube.

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
