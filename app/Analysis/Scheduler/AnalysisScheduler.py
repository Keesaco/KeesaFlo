###########################################################################
## \file app/Analysis/Scheduler/AnalysisScheduler.py
## \brief Defines the Analysis Scheduler which is responsible for scheduling tasks and providing information about the next task to be performed.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.Scheduler.AnalysisScheduler
## \brief Provides the analysis scheduler class for task scheduling
###########################################################################


## \brief Analysis Scheduler responsible for scheduling analysis instantiations.
class AnalysisScheduler:
	
	###########################################################################
	## \brief Constructor for AnalysisScheduler.
	## \param self - instance reference
	## \return Returns the AnalysisScheduler instance.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self	):
		pass

	###########################################################################
	## \brief Is called to add a task to the schedule to be queued for analysis.
	## \param analysis_id - the id of the task being queued
	## \param priority - a value determining the priority of the specific analysis
	## \return On fail, return False. On success, return True.
	## \note If an analysis_id already exists in the queue, then it will be merged.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def schedule_task( 	analysis_id,
						priority	):
		pass

	###########################################################################
	## \brief Is called to add remove a task from the schedule.
	## \param analysis_id - the id of the task being queued
	## \return If task removed, return True. If task does not exist in list, return False.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def remove_task(	analysis_id	):
		pass
		
	###########################################################################
	## \brief Checks to see whether the analysis_id exists in the queue and if so where.
	## \param analysis_id - the id of the task to be checked for
	## \return If task not in schedule, return false. Else, return the current priority of the task.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_task(	analysis_id	):
		pass
	
	###########################################################################
	## \brief Is called to return the next item to be analysed according to the schedule.
	## \return Returns the analysis_id of the first element in the schedule. Return False on fail.
	## \note Will fail if there are no elements in the schedule.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def next_task(	):
		pass

	###########################################################################
	## \brief Is called to return how many tasks are currently in the schedule.
	## \return Returns the number of tasks currently in the schedule.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def number_task(	):
		pass

