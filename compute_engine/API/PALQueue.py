###########################################################################
## \file compute_engine/API/PALQueue.py
## \brief Contains the PALQueue package: Platform Abstraction Layer for task queue access.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.API.PALQueue
## \brief Contains abstraction layer functions for Google taskqueue - returns results in a platform independent form. For use on Google Compute Engine.
## \brief Provides an API for accessing the job queue as a consumer.
###########################################################################

from oauth2client import gce
from apiclient.discovery import build
import httplib2
from base64 import b64decode

## Constants.
PROJECT_ID = 's~keesaco-spe'

###########################################################################
## \brief Authenticates an http connection for use with Google APIs.
## \return An authenticated http connection.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def auth():
	credentials = gce.AppAssertionCredentials('')
	auth_http = credentials.authorize(httplib2.Http())
	credentials.refresh(auth_http)
	return auth_http

###########################################################################
## \brief Builds a taskqueue task Google API.
## \return Built taskqueue task API.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def build_api():
	service = build('taskqueue', 'v1beta2', http = auth())
	return service.tasks()

###########################################################################
## \brief Leases a task from the task queue.
## \param queue - name of queue to lease from.
## \return a tuple containing the task id, then a list of command strings in the leased task. If there are no tasks returns None.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def lease(	queue_name, leaseTime ):
	## Build Google task queue API.
	tq = build_api()
	## Execute lease request.
	response = tq.lease(project = PROJECT_ID,
		leaseSecs = leaseTime,
		numTasks = 1,
		taskqueue = queue_name
		).execute()
	## Get task if queue is not empty, else return list containing empty string.
	if 'items' in response:
		## Get task from response.
		task = response['items'][0]
		## Get payload from task.
		payload = b64decode(task['payloadBase64'])
		## Get commands from payload.
		commands = payload.split(';')
		## Get task id.
		task_id = task['id']
		## Return id and commands.
		return (task_id, commands)
	else:
		return None

###########################################################################
## \brief Deletes a task from the task queue.
## \param queue - name of queue to delete from.
## \param task_id - the unique id of the task to delete.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def delete(	queue_name, task_id ):
	## Build Google task queue API.
	tq = build_api()
	## Execute delete request.
	response = tq.delete(project = PROJECT_ID,
		task = task_id,
		taskqueue = queue_name
	).execute()
