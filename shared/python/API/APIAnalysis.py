## \file shared/python/API/APIAnalysis.py
# \brief Defines the analysis API for analysing data. Built upon PALAnalysis for cross-platform support.
# \author swhitehouse@keesaco.com of Keesaco
# \author rmurley@keesaco.com of Keesaco

from PALAnalysis import *

## \brief Second tier API for analysis - Utilises PAL for platform specific analysis - Manages requests to the Analysis API.
class AnalysisManager:

	## \brief Constructor for AnalysisManager.
	# \param self - instance reference
	# \return Returns the AnalysisManager instance.
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(	self	):
		pass

	## \brief Is called to request that a new analysis using a specific plugin and data set be added to the scheduler.
	# \param data_ref - reference to the data to be analysis
	# \param plugin_ref - reference to the plugin to be used for analysis
	# \param user_id - the id of the user starting the analysis
	# \param priority - a value determining the priority of the specific analysis
	# \return On fail, return false. On success, returns the analysis_id for the specific analysis request.
	# \note user_id is used primarily to make sure that other users cannot mess with the original user's analysis.
	# \warning This function does not check that the user has permissions to perform the specified analysis. Nor does it check whether the analysis has already been performed.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def queue_analysis(	data_ref,
						plugin_ref,
						user_id,
						priority	):
		pass
	
	## \brief Requests that the specific analysis instantiation is ended prematurely.
	# \param analysis_id - the id of the analysis that needs to be ended
	# \param user_id - the id of the user ending the analysis
	# \return If analysis termination is successful, return True. Else False.
	# \note May not actually cancel analysis, unless all users related to that analysis request for it to be cancelled.
	# \note Will fail if the user_id does not match stored values in the analysis_id.
	# \note Will fail if the analysis_id does not exist.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def cancel_analysis(	analysis_id,
							user_id	):
		pass

	## \brief Requests that the priority of a currently running analysis instantiation is changed.
	# \param analysis_id - the id of the analysis that is having its priority changed
	# \param user_id - the id of the user changing the priority
	# \param priority - a value determining the priority that the analysis needs to be changed to
	# \return If analysis priority change is successful, return True. Else False.
	# \note Will fail if the user_id does not match stored values in the analysis_id.
	# \note Will fail if the analysis_id does not exist.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def change_priority(	analysis_id,
							user_id,
							priority	):
		pass

	## \brief Requests that the current state of the analysis is checked.
	# \param analysis_id - the id of the analysis that is being checked
	# \param user_id - the id of the user checking the analysis
	# \returns Returns information on the current state of the analysis. If failed, return False.
	# \note Will either return the analysis' position in the schedule, or the expected time remaining on the actual analysis.
	# \note Will fail if the user_id does not match stored values in the analysis_id.
	# \note Will fail if the analysis_id does not exist.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def check_analysis(	analysis_id,
						user_id	):
		pass

## \brief Second tier API for analysis - Utilises PAL for platform specific analysis - Schedules analysis.
class AnalysisSchedule:

	## \brief Constructor for AnalysisSchedule.
	# \param self - instance reference
	# \return Returns the AnalysisSchedule instance.
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(	self	):
		pass

	## \brief Is called to add a task to the schedule to be queued for analysis.
	# \param analysis_id - the id of the task being queued
	# \param priority - a value determining the priority of the specific analysis
	# \return On fail, return False. On success, return True.
	# \note If an analysis_id already exists in the queue, then it will be given the higher priority out of the new priority and its existing priority.
	# \author swhitehouse@keesaco.com of Keesaco
	def schedule_task( 	analysis_id,
						priority	):
		pass

	## \brief Is called to add remove a task from the schedule.
	# \param analysis_id - the id of the task being queued
	# \return If task removed, return True. If task does not exist in list, return False.
	# \author swhitehouse@keesaco.com of Keesaco
	def remove_task(	analysis_id	):
		pass
		
	## \brief Checks to see whether the analysis_id exists in the queue and if so where.
	# \param analysis_id - the id of the task to be checked for
	# \return If task not in schedule, return false. Else, return the current priority of the task.
	# \author swhitehouse@keesaco.com of Keesaco
	def check_task(	analysis_id	):
		pass
	
	## \brief Is called to return the next item to be analysed according to the schedule.
	# \return Returns the analysis_id of the first element in the schedule. Return False on fail.
	# \note Will fail if there are no elements in the schedule.
	# \author swhitehouse@keesaco.com of Keesaco
	def next_task(	):
		pass

	## \brief Is called to return how many tasks are currently in the schedule.
	# \return Returns the number of tasks currently in the schedule. Return False on fail.
	# \author swhitehouse@keesaco.com of Keesaco
	def number_task(	):
		pass

