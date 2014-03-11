###########################################################################
## \file compute_engine/visualise.py
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.visualise
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Should be called by the Compute Engine startup sheel script. Depends on AnalysisAPI.
###########################################################################
import sys, os
import API.APIAnalysis as Ana

# Task queue imports.
from oauth2client import gce
from apiclient.discovery import build
import httplib2
from base64 import b64decode
import time

# Lease a task and return payload.
def lease_payload():
	credentials = gce.AppAssertionCredentials('')
	auth_http = credentials.authorize(httplib2.Http())
	credentials.refresh(auth_http)
	service = build('taskqueue', 'v1beta2', http = auth_http)
	tq = service.tasks()
	response = tq.lease(project = 's~keesaco-spe',
		leaseSecs = 30,
		numTasks = 1,
		taskqueue = 'jobs'
		).execute()
	# Get task from response.
	if 'items' in response:
		task = response['items'][0]
		# Get payload from task.
		payload = b64decode(task['payloadBase64'])
		print payload
		# Get commands from payload.
		return payload.split(';')
	else:
		print 'No commands.'
		return ['']

# Check task queue.
while True:
	# Lease a command.
	commands = lease_payload()
	# If command is to kill instance, break out of loop and exit python script.
	if (commands[0] == 'kill'):
		break
	# If command is to visualise, visualise.
	if (commands[0] == 'vis'):
		# Get name.
		name = commands[1]
		## Load raw fcs data from cloud storage.
		Ana.load_fcs(name)
		## Create visualisation of raw fcs data.
		Ana.visualise(name)
		## Save visualisation to cloud storage.
		Ana.save_vis(name + '.png')
		## Clean up.
		os.remove(name)
		os.remove(name + '.png')
	# Wait before checking queue again.
	time.sleep(1)
