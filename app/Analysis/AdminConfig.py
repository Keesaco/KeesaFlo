###########################################################################
## \file app/Analysis/ExtAdminConfig.py
## \brief Contains 'administration' variables which changes the functioning of the analysis package.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.ExtAdminConfig
## \brief Provides administrative variables to control the functioning of the package.
###########################################################################


## \brief Contains variable to control the analysis system.
class ExtAdminConfig:

	###########################################################################
	## \brief Constructor for AdminVariables.
	## \param self - instance reference
	## \param max_tasks_per_user - (= 2) the maximum number of concurrent task any user can run
	## \param max_tasks_total - (= 10) the maximum total concurrent task that can be run
	## \param max_priority - (= 50) the maximum priority any user can have
	## \return Returns the AdminVariables instance.
	## \note In each variable, use of '0' denotes infinite.
	## \note e.g. if max_priority = 0 then the maximum priority is unlimited by the system.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					max_tasks_per_user = 2,
					max_tasks_total = 10,
					max_priority = 50	):
		if max_tasks_per_user < 0:
			max_tasks_per_user = 1
		## Defines the maximum number of analysis tasks a user can have running at any one time.
		self.max_tasks_per_user = max_tasks_per_user
		if max_tasks_total < 0:
			max_tasks_total = 1
		## Defines the maximum total tasks the system can handle at any one time.
		self.max_tasks_total = max_tasks_total
		if max_priority < 0:
			max_priority = 1
		## Defines the maximum priority of any user.
		self.max_priority = max_priority
		pass

	

