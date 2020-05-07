# This code will build elasticube through API

import requests
import urllib3
import os

def buildEcube(ecube, usern, passw):

    url = 'http://localhost:8083/api/v1/authentication/login'  # URL to generate API token

    header = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}  # Headers to be used with URL in POST request

    myobj = {'username': usern, 'password': passw}  # Data to be passed with URL in POST request

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # To disable warnings in output

    response = requests.post(url, headers=header, data=myobj, verify=False)  # POST request to generate API Token

    my_json = response.json()  # Converting output to json format

    token = my_json['access_token']  # Retrieving the value of access_token from json output. This is the Token, which will be used for further actions.

    ecubeBuildUrl = 'http://localhost:8083/api/elasticubes/localhost/' + ecube + '/startBuild?type=Full'  # URL to build ecube with build type

    withHeader = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + (token)}  # Headers to be used with URL in POST request

    statusUrl = 'http://localhost:8083/api/elasticubes/servers/localhost/status'
    statusHeader = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + (token)}
    statusResponse = requests.get(statusUrl, headers=statusHeader, verify=False)
    statusResponseLoadJson = statusResponse.json()
    #print(statusResponseLoadJson)

    for statusData in statusResponseLoadJson:
        if statusData['title'] == ecube:
            if statusData['status'] == 514 or statusData['status'] == 2048:
                print(statusData['title'] + ' is already processing. Please wait!')
            else:
                ecubebuildResponse = requests.post(ecubeBuildUrl, headers=withHeader, verify=False)  # POST request to build elasticube

                if ecubebuildResponse.status_code == 200:
                    print('Build started for ' + ecube)
                else:
                    print('Build failed for ' + ecube)

    #print(ecubebuildResponse.status_code)

if __name__ == "__main__":

    newlist = []
    list = os.listdir("C:\\Program Files\\Sisense\\Samples\\Sources")
    for element in list:
        if element[-6:] == '.ecube':
            #newelement = element[:-6]
            newlist.append(element[:-6])
    print(newlist)
    for ecube in newlist:
        buildEcube(ecube, 'deepak.sahu2@ge.com', 'Test123!')  # Calling function with eCube name, username and password parameters to build eCube.

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

    # The status of the ElastiCube
    # ============================
    # 1 - stopped
    # 2 - running
    # 4 - faulted
    # 8 - being deleted
    # 16 - currently restarting
    # 32 - wrong version
    # 64 - the ElastiCube is down because it is 32 bit data on a 64 bit codebase
    # 128 - the ElastiCube is down because it is 64 bit data on a 32 bit codebase
    # 256 - locked
    # 514 - the ElastiCube or its child is currently in a build process.
    # 1024 - the ElastiCube is starting, but not yet running.
    # 2048 - the ElastiCube is in a build process.
    # 4096 - trying to import a BigData ElastiCube on a non - BigData server
    # 8192 - trying to import a non - BigData ElastiCube on a BigData server
    # 16384 - Building is finished, now post indexing is running
    # 32768 - the ElastiCube is being stopped but its executable is still running
    # 65536 - this ElastiCube is in the process of cancelling an in -progress build
