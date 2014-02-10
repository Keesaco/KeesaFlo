###########################################################################
## \file app/Analysis/ComputeEngine/GCEManager.py
## \brief Contains types and functions for managing instances.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.ComputeEngine.GCEManager
## \brief Contains types and functions for managing instances on Compute Engine.
###########################################################################

import logging
import sys
import argparse
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.tools import run_flow
from apiclient.discovery import build
from Analysis.ComputeEngine.ComputeEngineConfig import *

## \brief Manager which tracks all instances within the scope of the project on Compute Engine.
class GCEManager:

	###########################################################################
	## \brief Constructor for the GCEManager object.
	## \param self - instance reference
	## \return Returns GCEManager object on success.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(self):
		# Sets up logging for command line debugging
		logging.basicConfig(level=logging.ERROR)

		# Sets up flags for use in authentication flow
		parser = argparse.ArgumentParser(
			description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			parents=[tools.argparser])
		flags = parser.parse_args()
		
		# Perform OAuth 2.0 authorisation.
		flow = flow_from_clientsecrets(SECRETS_URL, scope=GCE_SCOPE)
		storage = Storage(STORAGE_URL) # Stores temporary access data 
		credentials = storage.get()
		if credentials is None or credentials.invalid:
			credentials = run_flow(flow, storage, flags)
		
		# Sets up http authorisation using OAuth 2.0 credentials
		http = httplib2.Http()
		## The authorised http channel to use for communication.
		self.auth_http = credentials.authorize(http)

		# Initialises compute engine service
		## The Google Compute Engine Service to communicate with.
		self.gce_service = build('compute', API_VERSION)
		project_url = GCE_URL + PROJECT_ID
		
		## The Persistent Disk objects running on compute engine.
		self.persistent_disks = []
		## Bool to determine if persistent disks have been created yet.
		self.pds_present = False
		
		# Creates instances
		for i in range(0, MAX_INSTANCES):
			self.persistent_disks.append(PersistentDisk(i, self.gce_service, self.auth_http))
		self.pds_present = True
		
		self.counter = 0
		self.instance_names = []

	###########################################################################
	## \brief Creates persistent disk up to the max number of instances.
	## \param self - instance reference
	## \return Returns True on success, False on fail.
	## \note Will fail if the persistent disks already exist.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def start_pds(self):
		if self.pds_present == False:
			for persistent_disk in self.persistent_disks:
				persistent_disk.start_pd()
			self.pds_present = True
			return True
		return False
	
	###########################################################################
	## \brief Starts an instance on the first available persistent disk.
	## \param self - instance reference
	## \param instance_name - the name of the new instance
	## \param file_location - the name of the file to be processed
	## \return Returns True on success, False on fail.
	## \note Will fail if there are no persistent disks available.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def start_instance_pd(self, instance_name, file_location):
		self.instance_names = {file_location : 'keesaflo-analysis-' + str(self.counter)}
		self.counter += 1
		for persistent_disk in self.persistent_disks:
			if persistent_disk.instance_name == "":
				persistent_disk.start_instance(self.instance_names[file_location], file_location)
				return True
		return False
	
	###########################################################################
	## \brief Terminates an instance.
	## \param self - instance reference
	## \param instance_name - the name of the instance to be deleted
	## \return Returns True on success, False on fail.
	## \note Will fail if the instance does not exist.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def terminate_instance_pd(self, instance_name):
		for persistent_disk in self.persistent_disks:
			if persistent_disk.instance_name == self.instance_names[instance_name]:
				persistent_disk.terminate_instance()
				return True
		return False

	###########################################################################
	## \brief Terminates all instances and deletes persistent disks.
	## \param self - instance reference
	## \return Returns True on success, False on fail.
	## \note Will fail if there are currently no persistent disks.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def terminate_pds(self):
		if self.pds_present == True:
			for persistent_disk in self.persistent_disks:
				if persistent_disk.instance_name != "":
					persistent_disk.terminate_instance()
				persistent_disk.terminate_pd()
			self.pds_present = False
			return True
		return False


## \brief A PersistentDisk class which tracks an individual persistent disk on Compute Engine.	
class PersistentDisk:
	
	###########################################################################
	## \brief Constructor for the PersistentDisk object.
	## \param self - instance reference
	## \param id - the unique id number of the persistent disk
	## \param gce_service - the gce service to communicate with
	## \param auth_http - the http channel to send communication down
	## \return Returns PersistentDisk object on success.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, id, gce_service, auth_http):
		## The unique name of the persistent disk.
		self.pd_name = DEFAULT_PD_NAME + str(id)
		## The gce service to be communicated down.
		self.gce_service = gce_service
		## The http channel to send communication down.
		self.auth_http = auth_http
		## Bool to determine if the persistent disk has been created.
		self.pd_present = False
		## Name of the instance currently running on this persistent disk ('""' if none).
		self.instance_name = ""
		self.start_pd()
	
	###########################################################################
	## \brief Creates persistent disk.
	## \param self - instance reference
	## \return Returns True on success, False on fail.
	## \note Will fail if the persistent disk already exist.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def start_pd(self):
		if self.pd_present == False:
			request = self.gce_service.disks().insert(
				project=PROJECT_ID, body={
					'name': self.pd_name
					},
				zone=DEFAULT_ZONE, sourceImage=IMAGE_URL)
			block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))
			self.pd_present = True
			return True
		return False
	
	###########################################################################
	## \brief Starts an instance on this persistent disk.
	## \param self - instance reference
	## \param instance_name - the name of the new instance
	## \param file_location - the name of the file to be processed
	## \return Returns True on success, False on fail.
	## \note Will fail if there is already an instance running on this disk.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def start_instance(self, instance_name, file_location):
		if self.instance_name == "":
			self.instance_name = instance_name
			instance = create_instance_request(self.pd_name, self.instance_name, file_location)
			request = self.gce_service.instances().insert(
				project=PROJECT_ID, body=instance, zone=DEFAULT_ZONE)
			block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))
			return True
		return False
		
	###########################################################################
	## \brief Terminates the instance on this persistent disk instance.
	## \param self - instance reference
	## \return Returns True on success, False on fail.
	## \note Will fail if there is no instance on this disk.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def terminate_instance(self):
		if self.instance_name != "":
			request = self.gce_service.instances().delete(
				project=PROJECT_ID, instance=self.instance_name, zone=DEFAULT_ZONE)
			block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))
			self.instance_name = ""
			return True
		return False
	
	###########################################################################
	## \brief Terminates the instance and deletes the persistent disk.
	## \param self - instance reference
	## \return Returns True on success, False on fail.
	## \note Will fail if there is currently not a persistent disk.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def terminate_pd(self):
		if self.pd_present == True:
			if self.instance_name != "":
				self.terminate_instance()
			request = self.gce_service.disks().delete(
				disk=self.pd_name, project=PROJECT_ID, zone=DEFAULT_ZONE)
			block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))
			self.pd_present = False
			return True
		return False


###########################################################################
## \brief Creates the JSON for an instance request.
## \param pd_name - the persistent disk to create the instance on.
## \param instance_name - the name of the instance to be created
## \param file_location - the location of the file to be analysed
## \return Returns the JSON for the request body of the new instance.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################		
def create_instance_request(pd_name, instance_name, file_location):
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
				}, {
				'key': 'file_location',
				'value': file_location
				}]
			}]	
		}


###########################################################################
## \brief Forces waiting until the current request has been completed.
## \param gce_service - the Google Compute Engine service to communicate with
## \param auth_http - the authorised http channel to send the request down
## \param response - the response from the request to be waited for.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def block_until_done(gce_service, auth_http, response):

	status = response['status']
	while status != 'DONE' and response:
		operation_id = response['name']

		# Identify if this is a per-zone resource
		if 'zone' in response:
			zone_name = response['zone'].split('/')[-1]
			request = gce_service.zoneOperations().get(
				project=PROJECT_ID,
				operation=operation_id,
				zone=zone_name)
		else:
			request = gce_service.globalOperations().get(
				project=PROJECT_ID, operation=operation_id)

		response = request.execute(http=auth_http)
		if response:
			status = response['status']

