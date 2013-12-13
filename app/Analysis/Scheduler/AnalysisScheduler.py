###########################################################################
## \file app/Analysis/Scheduler/AnalysisScheduler.py
## \brief Defines the Analysis Scheduler which is responsible for scheduling tasks and providing information about the next task to be performed.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.Scheduler.AnalysisScheduler
## \brief Provides the analysis scheduler class for task scheduling
###########################################################################
	
from app.Analysis.Types import ScheduleQueue
from app.Analysis import AdminConfig

## The schedule queue variable which holds the actual queue object.
schedule_queue = ScheduleQueue()
	
###########################################################################
## \brief Is called to add a task to the schedule to be queued for analysis.
## \param analysis_id - the id of the task being to be added to
## \param user_id - the id of the user to be added
## \param priority - (= 1) a value determining the priority for the user.
## \return On fail, return False. On success, return True.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def add_user_task( 	analysis_id,
					user_id,
					priority = 1	):
	if priority > AdminConfig.max_priority:
		priority = AdminConfig.max_priority
	if schedule_queue.check_user(user_id) >= AdminConfig.max_tasks_per_user:
		return False
	if schedule_queue.add_user_to_element(analysis_id, user_id, priority):
		schedule_queue.age_queue()
		return True
	return False

###########################################################################
## \brief Is called to add remove a task from the schedule.
## \param analysis_id - the id of the task being queued
## \return If task removed, return True. If task does not exist in list, return False.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def remove_user_task(	analysis_id,
						user_id	):
	if schedule_queue.remove_user_from_element(analysis_id, user_id):
		schedule_queue.age_queue()
		return True
	return False
		
###########################################################################
## \brief Checks to see whether the analysis_id exists in the queue and if so where.
## \param analysis_id - the id of the task to be checked for
## \return If task not in schedule, return false. Else, return the current priority of the task.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def check_task(	analysis_id	):
	return schedule_queue.check_element(analysis_id)
	
###########################################################################
## \brief Is called to return the next item to be analysed according to the schedule.
## \return Returns the analysis_id of the first element in the schedule. Return False on fail.
## \note Will fail if there are no elements in the schedule.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def next_task(	):
	return schedule_queue.next_element()

###########################################################################
## \brief Is called to return how many tasks are currently in the schedule.
## \return Returns the number of tasks currently in the schedule.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def number_task(	):
	return schedule_queue.check_number_elements()

###########################################################################
## \brief A useful function for debugging which will print out the queue information
## \param self - instance reference
## \param prefix - (= "")a string to be placed before each string printed by the function.
## \return Returns nothing.
## \note Due to the problems with printing to a console in multi-element programs, this function should only be user for debugging.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################	
def print_queue(	):
	print ("%%%%%%%%%%%%%%%%%%%%%%%%%")
	schedule_queue.print_queue("%% ")
	print ("%%%%%%%%%%%%%%%%%%%%%%%%%")

