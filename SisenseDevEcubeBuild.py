# This code will build elasticube through API

import requests
import urllib3

def buildEcube(ecube, usern, passw):

    url = "https://dev.sisense.digital.ge.com/api/v1/authentication/login"  # URL to generate API token

    header = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}  # Headers to be used with URL in POST request

    myobj = {'username': usern, 'password': passw}  # Data to be passed with URL in POST request

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # To disable warnings in output

    response = requests.post(url, headers=header, data=myobj, verify=False)  # POST request to generate API Token

    my_json = response.json()  # Converting output to json format

    token = my_json['access_token']  # Retrieving the value of access_token from json output. This is the Token which will be used for further actions.

    ecubeBuildUrl = 'https://dev.sisense.digital.ge.com/api/elasticubes/localhost/' + ecube + '/startBuild?type=Full'  # URL to build ecube with build type

    withHeader = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + (token)}  # Headers to be used with URL in POST request

    ecubebuildResponse = requests.post(ecubeBuildUrl, headers=withHeader, verify=False)  # POST request to build elasticube

    print(ecubebuildResponse)  # Printing the response code


if __name__ == "__main__":

    # buildEcube('3PS Analytics', 'admin@ge.com', 'Sisense@GE123')  # Calling function with eCube name, username and password parameters to build eCube.
    # Uncomment the above line to run it


    # NOTES:

    # HTTP Status Codes
    # =================
    # 200   Success
    # 400	invalid elasticube or server
    # 403	forbidden

    # Build Types
    # ===========
    # None - Updates the ElastiCube server with the ElastiCube schema, without building.
    # Full - Rebuilds the ElastiCube from scratch.
    # Delta - Rebuilds from scratch tables that have changed in the ElastiCube schema.
    # FullUpdateExisting - Rebuilds the ElastiCube and accumulates data for tables marked as accumulative. This mode should only be used for accumulative builds.

