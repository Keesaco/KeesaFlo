###########################################################################
## \file app/API/PALQueue.py
## \brief Contains the PALQueue package: Platform Abstraction Layer for task queue access.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALQueue
## \brief Contains abstraction layer functions for Google taskqueue - returns results in a platform independent form
## \brief Provides an API for accessing the job queue.
###########################################################################

from google.appengine.api import taskqueue

###########################################################################
## \brief Adds a task to the Google Task Queue.
## \param queue - name of a Google Task pull queue to add task to
## \param task - task payload string
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def add_task(	queue, task ):
	q = taskqueue.Queue(queue)
	tasks = []
	tasks.append(taskqueue.Task(payload = task, method = 'PULL'))
	q.add(tasks)
