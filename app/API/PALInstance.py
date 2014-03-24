###########################################################################
## \file app/API/PALInstance.py
## \brief Contains the PALInstance package: Platform Abstraction Layer for instance management.
## \author rmurley@keesaco.com of Keesaco
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALInstance
## \brief Contains abstraction layer functions for Google Compute Engine instances - returns results in a platform independent form
## \brief Provides an API for starting and monitoring Google Compute Engine instances.
###########################################################################

from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
import httplib2
from Analysis.ComputeEngine.ComputeEngineConfig import *
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.tools import run_flow
from apiclient.discovery import build

###########################################################################
## \brief Authenticates an http connection for use with Google APIs.
## \return An authenticated http connection.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def auth():
	# Open private key file and read in private key
	f = file(PRIVATE_KEY_URL, 'rb')
	key = f.read()
	f.close()
	# Uses the service account email and private key to verify credentials
	credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key, GCE_SCOPE)
	## The authorised http channel to use for communication.
	return credentials.authorize(httplib2.Http())

###########################################################################
## \brief Builds a Compute Engine Google API.
## \return Built Compute Engine API.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def build_api():
	return build('compute', API_VERSION, http = auth())

###########################################################################
## \brief Counts the number of active Compute Engine Instances.
## \return Returns the number of active Compute Engine Instances.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def count():
	gce_api = build_api().instances()
	resp = gce_api.aggregatedList(project = PROJECT_ID, key = DEFAULT_ZONE).execute()
	instance_info = resp['items']['zones/' + DEFAULT_ZONE]
	if 'warning' in instance_info:
		return 0
	else:
		return len(instance_info['instances'])

###########################################################################
## \brief Builds JSON body for an instance request.
## \param pd_name - the persistent disk to create the instance on.
## \param instance_name - the name of the instance to be created
## \return Returns the JSON for the request body of the new instance.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################		
def instance_request_body(pd_name, instance_name):
	return {
		'name': instance_name,
		'machineType': MACHINE_TYPE_URL,
		'disks': [{
			'source': '%s/disks/%s' % (ZONE_URL, pd_name),
			'boot': 'true',
			'type': 'PERSISTENT'
			}],
		'networkInterfaces': [{
			'accessConfigs': [{
				'type': 'ONE_TO_ONE_NAT',
				'name': 'External NAT'
				}],
			'network': NETWORK_URL
			}],
		'serviceAccounts': [{
			'email': DEFAULT_SERVICE_EMAIL,
			'scopes': DEFAULT_SCOPES
			}],
		'metadata': [{
			'items': [{
				'key': 'startup-script',
				'value': open(STARTUP_URL, 'r').read()
				},{
				'key': 'instance_name',
				'value': instance_name
				}]
			}]	
		}

###########################################################################
## \brief Starts a new Compute Engine Instance.
## \param instance_name - name of instance to start.
## \param disk_name - name of persistent disk to use.
## \return returns JSON response to REST API request.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def start(instance_name, disk_name):
	gce_api = build_api().instances()
	body = instance_request_body(disk_name, instance_name)
	return gce_api.insert(	project = PROJECT_ID,
							body = body,
							zone = DEFAULT_ZONE
							).execute()

###########################################################################
## \brief Creates a new persistent disk
## \param disk_name - name of disk to create.
## \return returns JSON response to REST API request.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def create_disk(disk_name):
	gce_api = build_api().disks()
	resp = gce_api.insert(	project = PROJECT_ID,
							body={'name': disk_name},
							zone = DEFAULT_ZONE,
							sourceImage = IMAGE_URL
							).execute()
	return wait_for_response(resp)

###########################################################################
## \brief Forces waiting until the current request has been completed.
## \param response - the response from the request to be waited for.
## \return returns the response from the request
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def wait_for_response(response):
	gce_service = build_api()
	auth_http = auth()
	status = response['status']
	while status != 'DONE' and response:
		operation_id = response['name']

		# Identify if this is a per-zone resource
		if 'zone' in response:
			zone_name = response['zone'].split('/')[-1]
			request = gce_service.zoneOperations().get(
				project = PROJECT_ID,
				operation = operation_id,
				zone = zone_name)
		else:
			request = gce_service.globalOperations().get(
				project = PROJECT_ID, operation = operation_id)

		response = request.execute(http = auth_http)
		if response:
			status = response['status']

	return response
