###########################################################################
## \file app/Analysis/Manager/AnalysisManager.py
## \brief Defines the Analysis Manager which is responsible for managing analysis tasks.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.Manager.AnalysisManager
## \brief Provides an Analysis Manager class which is responsible for managing analysis tasks.
###########################################################################

from app.Analysis.Manager import PALAnalysisManager
from app.Analysis.Scheduler import AnalysisScheduler
from app.Analysis import AdminConfig
from app.Analysis.Types import RequestList
from app.Analysis.Manager.GCEManager import GCEManager

## The RequestList object which will hold information on analysis requests.
request_list = RequestList()
gce_manager = GCEManager()

###########################################################################
## \brief Is called to add a user to an analysis task using the required plugin and dataset.
## \param file_location - the location of the file to be analysed
## \return Returns the analysis_id of the analysis task added to. On fail, returns False.
## \note Will fail if the user has already been added to the analysis task.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def new_analysis_task(	file_location	):
	return gce_manager.start_instance_pd(file_location)
	

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

