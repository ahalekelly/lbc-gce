#!/usr/bin/python3
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os
from datetime import datetime

print("\n"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'beta', credentials=credentials)

project = os.popen("gcloud config list --format 'value(core.project)'").read().strip()

request = service.zones().list(project=project)
while request is not None:
    response = request.execute()
    zones = [zone['name'] for zone in response['items']]
    request = service.zones().list_next(previous_request=request, previous_response=response)


for zone in zones:
    request = service.instances().list(project=project, zone=zone)
    while request is not None:
        response = request.execute()
#        print(zone)
        if 'items' in response:
            for instance in response['items']:
                print(instance['name']+" "+instance['status'])
                if instance['status'] != 'RUNNING':
                    print("starting: "+instance['name'])
                    startRequest = service.instances().start(project=project, zone=zone, instance=instance['name'])
                    startResponse = startRequest.execute()

        request = service.instances().list_next(previous_request=request, previous_response=response)
