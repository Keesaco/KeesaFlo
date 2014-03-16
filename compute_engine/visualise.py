###########################################################################
## \file compute_engine/visualise.py
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.visualise
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Should be called by the Compute Engine startup sheel script. Depends on AnalysisAPI.
###########################################################################
import os
import API.APIAnalysis as Ana
import API.APIQueue as Queue

# Check task queue until 'kill' command is received.
alive = True
while alive:
	# Lease a command.
	task = Queue.lease('jobs', 30)
	# If there are tasks in queue extract id and commands, else restart loop and check queue again.
	if task is not None:
		task_id = task[0]
		commands = task[1]
	else:
		continue
	# If command is to kill instance, stop looping and exit python script.
	if (commands[0] == 'kill'):
		alive = False
	# If command is to visualise, visualise.
	elif (commands[0] == 'vis'):
		# Get name.
		name = commands[1]
		## Load raw fcs data from cloud storage.
		Ana.load_fcs(name)
		## Create visualisation of raw fcs data.
		Ana.visualise(name)
		## Save visualisation to cloud storage.
		Ana.save_vis(name + '.png')
		## Clean up.
		os.remove(name)
		os.remove(name + '.png')
	# Delete any processed tasks from queue.
	if task_id is not None:
		Queue.delete('jobs', task_id)
