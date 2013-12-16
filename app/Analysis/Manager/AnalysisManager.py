###########################################################################
## \file app/Analysis/Manager/AnalysisManager.py
## \brief Defines the Analysis Manager which is responsible for instantiating plugins and providing information to the instantiations.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.Manager.AnalysisManager
## \brief Provides an Analysis Manager class which is responsible for instantiating plugins and providing information to the instantiations.
###########################################################################

from app.Analysis.Manager import PALAnalysisManager
from app.Analysis.Scheduler import AnalysisScheduler
from app.Analysis import AdminConfig
from app.Analysis.Types import RequestList

## The RequestList object which will hold information on analysis requests.
request_list = RequestList()

###########################################################################
## \brief Is called to add a user to an analysis task using the required plugin and dataset.
## \param user_id - the id of the user to be added
## \param priority - a value determining the priority for the user.
## \param data_location - the DataLocation objects containing information on the data to be used
## \param plugin_location - the PluginLocaiton object containing information on the plugin to be used
## \return Returns the analysis_id of the analysis task added to. On fail, returns False.
## \note Will fail if the user has already been added to the analysis task.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def subscribe_user_analysis(	user_id,
								priority,
								data_location,
								plugin_location	):
	analysis_id = request_list.subscribe_user(user_id, data_location, plugin_location)
	if analysis_id == False:
		return False
	if priority > AdminConfig.max_priority:
		priority = AdminConfig.max_priority
	if request_list.requests[analysis_id].being_analysed == False:
		if AnalysisScheduler.check_user(user_id) < AdminConfig.max_tasks_per_user:
			if AnalysisScheduler.add_user_task(analysis_id, user_id, priority) == False:
				request_list.unsubscribe_user(analysis_id, user_id)
				return False
			if request_list.requests[analysis_id].in_queue == False:
				request_list.change_state_request(analysis_id, True, False)
	return analysis_id

###########################################################################
## \brief Is called to remove a user from an analysis task.
## \param analysis_id - the analysis id for the analysis that the user need to be removed from
## \param user_id - the id of the user to be removed
## \return Returns True on success, False on fail.
## \note Will fail if the user does not exist in the analysis task, or the analysis task itself does not exist.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################	
def unsubscribe_user_analysis(	analysis_id,
								user_id	):
	if analysis_id in request_list.requests:
		if request_list.requests[analysis_id].in_queue == True:
			if AnalysisScheduler.remove_user_task(analysis_id, user_id):
				return request_list.unsubscribe_user(analysis_id, user_id)
		return request_list.unsubscribe_user(analysis_id, user_id)
	return False
		
###########################################################################
## \brief Is called to check on the progress of an analysis task.
## \param analysis_id - the analysis id for the analysis that the user need to be removed from
## \param user_id - the id of the user to be removed
## \return Returns True if the analysis request is in the queue, False if not.
## \note Will not return anything if the user is not listed in the request.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def check_analysis(	analysis_id,
					user_id	):
	if user in request_list.requests[analysis_id].users:
		return request_list.requests[analysis_id].in_queue

###########################################################################
## \brief A useful function for debugging which will print out the list information for all requests.
## \return Returns nothing.
## \note Due to the problems with printing to a console in multi-element programs, this function should only be user for debugging.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################	
def print_analysis(	):
	print ("%%%%%%%%%%%%%%%%%")
	print ("---RequestList---")
	request_list.print_list("%% ")
	print ("%%%%%%%%%%%%%%%%%")
	print ("--ScheduleQueue--")
	AnalysisScheduler.print_queue("%% ")
	print ("%%%%%%%%%%%%%%%%%")

