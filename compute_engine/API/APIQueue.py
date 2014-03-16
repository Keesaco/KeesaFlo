###########################################################################
## \file compute_engine/API/APIQueue.py
## \brief Defines the queue API for leaseing and deleting task queue tasks.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.API.APIQueue
## \brief Defines the queue API for leaseing and deleting task queue tasks.
## \note Depends on PALQueue
## \sa compute_engine.API.PALQueue
###########################################################################

import API.PALQueue as queue

###########################################################################
## \brief Leases a task from the task queue.
## \param queue - name of queue to lease from.
## \param leaseTime - the number of seconds to hold the lease.
## \return a tuple containing the task id, then a list of command strings in the leased task. If there are no tasks returns None.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def lease(	queue_name, leaseTime ):
	return queue.lease(queue_name, leaseTime)

###########################################################################
## \brief Deletes a task from the task queue.
## \param queue - name of queue to delete from.
## \param task_id - the unique id of the task to delete.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def delete(	queue_name, task_id ):
	queue.delete(queue_name, task_id)
