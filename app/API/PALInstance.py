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
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.tools import run_flow
from apiclient.discovery import build

## Constants.
PROJECT_NAME = 'keesaco-spe'
PRIVATE_KEY = 'gce_assets/private_key.pem'
GCE_SCOPE = 'https://www.googleapis.com/auth/compute'
SERVICE_ACCOUNT_EMAIL = '41520595559-5smi2i2nlql32u488dr0ig5epladi0hq@developer.gserviceaccount.com'
ZONE = 'zones/europe-west1-a'

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
