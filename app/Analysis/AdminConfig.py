###########################################################################
## \file app/Analysis/AdminConfig.py
## \brief Contains 'administration' variables which changes the functioning of the analysis package.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.AdminConfig
## \brief Provides administrative variables to control the functioning of the package.
###########################################################################

## Defines the maximum number of analysis tasks a user can have running at any one time.
max_tasks_per_user = 2
## Defines the maximum total tasks the system can handle at any one time.
max_tasks_total = 10
## Defines the maximum priority of any user.
max_priority = 50

###########################################################################
## \brief Changes the max_tasks_per_user variable.
## \param new_value - the value that the variable will be changed to
## \return Does not return anything.
## \note Use of '0' allows each user an unlimited number of tasks.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
def change_max_tasks_user(	new_value	):
	if new_value < 0:
		new_value = 1
	max_tasks_per_user = new_value

###########################################################################
## \brief Changes the max_tasks_total variable.
## \param new_value - the value that the variable will be changed to
## \return Does not return anything.
## \note Use of '0' allows an unlimited number of tasks.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################	
def change_max_tasks_total(	new_value	):
	if new_value < 0:
		new_value = 1
	max_tasks_total = new_value

###########################################################################
## \brief Changes the max_priority variable.
## \param new_value - the value that the variable will be changed to
## \return Does not return anything.
## \note Use of '0' allows unlimited levels of priority per user.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################	
def change_max_priority(	new_value	):
	if new_value < 0:
		new_value = 1
	max_priority = new_value

