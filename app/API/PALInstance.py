###########################################################################
## \file app/API/PALInstance.py
## \brief Contains the PALInstance package: Platform Abstraction Layer for instance management.
## \author rmurley@keesaco.com of Keesaco
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
	f = file(PRIVATE_KEY, 'rb')
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
	service = build('compute', 'v1', http = auth())
	return service.instances()

###########################################################################
## \brief Counts the number of active Compute Engine Instances.
## \return Returns the number of active Compute Engine Instances.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def count():
	gce_api = instances.build_api()
	resp = gce_api.aggregatedList(project = PROJECT_NAME, key = ZONE).execute()
	instance_info = resp['items'][ZONE]
	if 'warning' in instance_info:
		return 0
	else:
		return len(instance_info['instances'])

###########################################################################
## \brief Starts a new Compute Engine Instance.
## \param type - type of instance to spin up.
## \return returns True if successful, false otherwise.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def start(	type	):
	gce_api = instances.build_api()
	resp = gce_api.aggregatedList(project = PROJECT_NAME, key = ZONE).execute()
	instance_info = resp['items'][ZONE]
	if 'warning' in instance_info:
		return 0
	else:
		return len(instance_info['instances'])

###########################################################################
## \brief Builds JSON for an instance request.
## \param pd_name - the persistent disk to create the instance on.
## \param instance_name - the name of the instance to be created
## \param file_location - the location of the file to be analysed
## \return Returns the JSON for the request body of the new instance.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################		
def build_request(pd_name, instance_name, file_location):
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
				},{
				'key': 'file_location',
				'value': file_location
				}]
			}]	
		}