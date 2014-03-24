###########################################################################
## \file app/Analysis/ComputeEngine/GCEManager.py
## \brief Contains types and functions for managing instances.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.ComputeEngine.GCEManager
## \brief Contains types and functions that manage instances on Compute Engine.
###########################################################################

import logging
import sys
import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
from Analysis.ComputeEngine.ComputeEngineConfig import *
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
		logging.basicConfig(level=logging.WARNING)

		# Open private key file and read in private key
		f = file(PRIVATE_KEY_URL, 'rb')
		key = f.read()
		f.close()

		# Uses the service account email and private key to verify credentials
		credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key, GCE_SCOPE)

		## The authorised http channel to use for communication.
		self.auth_http = credentials.authorize(httplib2.Http())

		## The Google Compute Engine Service to communicate with.
		self.gce_service = build('compute', API_VERSION)

		## The Persistent Disk objects running on compute engine.
		self.persistent_disks = []
		# Creates initial persistent disks
		for i in range(0, MAX_INSTANCES):
			self.persistent_disks.append(None)
		self.__pd_start()

	###########################################################################
	## \brief Creates an additional persistent disk.
	## \param self - instance reference
	## \return Returns True on success, False on fail.
	## \note Will fail if there is no more space for persistent disks.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __pd_start(self):
		for i in range(0, MAX_INSTANCES):
			if self.persistent_disks[i] == None:
				self.persistent_disks[i] = PersistentDisk(i, self.gce_service, self.auth_http)
				return True
		return False

	###########################################################################
	## \brief Deletes a persistent disk.
	## \param self - instance reference
	## \return Returns True on success, False on fail.
	## \note Will fail if there are no persistent disks to delete.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################		
	def __pd_terminate(self):
		for i in range(0, MAX_INSTANCES):
			if self.persistent_disks[i] != None:
				if self.persistent_disks[i].check_instance() == False:
					self.persistent_disks[i] = None
					return True				
		return False
	
	###########################################################################
	## \brief Checks the current number of persistent disks and instances and scales accordingly.
	## \param self - instance reference
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __pd_scale(self):
		num_instances = 0
		num_pds = 0
		for i in range(0, MAX_INSTANCES):
			if self.persistent_disks[i] != None:
				num_pds += 1
				if self.persistent_disks[i].check_instance():
					num_instances += 1
		num_instances += 1 + ((num_instances * CE_SCALING) / 10)
		if num_instances >= MAX_INSTANCES:
			num_instances = MAX_INSTANCES
		while num_pds < num_instances:
			if self.__pd_start():
				num_pds += 1		
		while num_pds > num_instances:
			if self.__pd_terminate():
				num_pds -= 1

	###########################################################################
	## \brief Starts an instance on the first available persistent disk.
	## \param self - instance reference
	## \param file_location - the name of the file to be processed
	## \return Returns True on success, False on fail.
	## \note Will fail if there are no persistent disks available.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def pd_start_instance(self, file_location):
		for i in range(0, MAX_INSTANCES):
			if self.persistent_disks[i] != None:
				if self.persistent_disks[i].check_instance() == False:
					if self.persistent_disks[i].start_instance(file_location):
						self.__pd_scale()
						return True
		return False

	###########################################################################
	## \brief Makes sure that when the object is deleted, it deletes all persistent disks and instances.
	## \param self - instance reference
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __del__(self):
		for i in range(0, MAX_INSTANCES):
			self.persistent_disks[i] = None


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
		## Name of the instance associated with this persistent disk.
		self.instance_name = DEFAULT_INSTANCE_NAME + str(id)
		self.check_string = 'name eq %s' % self.instance_name
		## The gce service to be communicated down.
		self.gce_service = gce_service
		## The http channel to send communication down.
		self.auth_http = auth_http
		## The request to create the persistent disk.
		request = self.gce_service.disks().insert(
			project=PROJECT_ID, body={
				'name': self.pd_name
				},
			zone=DEFAULT_ZONE, sourceImage=IMAGE_URL)
		## Blocking call until the persistent disk has been created.
		block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))
		## Boolean True if there is a chance that the instance exists.
		self.instance = False

	###########################################################################
	## \brief Checks for this disks instance on compute engine.
	## \param self - instance reference
	## \return Returns True if the instance exists, False if not.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_instance(self):
		if self.instance == True:
			request = self.gce_service.instances().list(
				project = PROJECT_ID, zone = DEFAULT_ZONE, filter = self.check_string)
			response = request.execute(http=self.auth_http)
			if 'items' in response:
				for item in response['items']:
					if item['name'] == self.instance_name:
						if item['status'] == 'RUNNING':
							return True
						else:
							return self.check_instance()
		self.instance = False
		return False

	###########################################################################
	## \brief Starts an instance on this persistent disk.
	## \param self - instance reference
	## \param file_location - the name of the file to be processed
	## \return Returns True on success, False on fail.
	## \note Will fail if there is already an instance running on this disk.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def start_instance(self, file_location):
		if self.check_instance() == False:
			instance = create_instance_request(self.pd_name, self.instance_name, file_location)
			request = self.gce_service.instances().insert(
				project=PROJECT_ID, body=instance, zone=DEFAULT_ZONE)
			response = block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))
			self.instance = True
			return True
		return False

	###########################################################################
	## \brief Makes sure that when the object is deleted, it deletes all persistent disks and instances.
	## \param self - instance reference
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __del__(self):
		if self.check_instance() == True:
			request = self.gce_service.instances().delete(
				project=PROJECT_ID, instance=self.instance_name, zone=DEFAULT_ZONE)
			block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))
		request = self.gce_service.disks().delete(
			disk=self.pd_name, project=PROJECT_ID, zone=DEFAULT_ZONE)
		block_until_done(self.gce_service, self.auth_http, request.execute(http=self.auth_http))


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
				},{
				'key': 'instance_name',
				'value': instance_name
				},{
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

