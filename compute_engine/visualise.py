###########################################################################
## \file compute_engine/visualise.py
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
## \author rmurley@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.visualise
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Should be called by the Compute Engine startup sheel script. Depends on AnalysisAPI.
###########################################################################
import os, time
import API.APIAnalysis as Ana
import API.APIQueue as Queue

# Check task queue until 'kill' command is received.
alive = True
while alive:
	# Lease a command.
	try:
		task = Queue.lease('jobs', 30)
	except errors.HttpError, e:
		print e
	except errors.BadStatusLine, e:
		print e
	# If there are tasks in queue extract id and commands, else restart loop and check queue again.
	if task is not None:
		task_id = task[0]
		commands = task[1]
	else:
		time.sleep(0.9)
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
		## Saves info about fcs file to cloud storage
		Ana.save_info(name + 'info.txt')
		## Clean up.
		os.remove(name)
		os.remove(name + '.png')
		os.remove(name + 'info.txt')
	elif (commands[0] == 'gate_rec'):
		name = commands[1]
		points = commands[2]
		gate_name = commands[3]
		coords = points.split()
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		##Creates visualisation of gate and text file of gate info
		Ana.rect_gate(name, gate_name, coords[0], coords[1], coords[2], coords[3])
		## Save visualisation to cloud storage.
		Ana.save_vis(gate_name + '.png')
		## Saves info about gate to cloud storage
		Ana.save_info(gate_name + '.txt')
		## Saves gate as fcs file
		Ana.save_fcs(gate_name)
		## Clean up.
		os.remove(name)
		os.remove(gate_name + '.txt')
		os.remove(gate_name + '.png')
		os.remove(gate_name)
	elif (commands[0] == 'gate_cir'):
		name = commands[1]
		points = commands[2]
		gate_name = commands[3]
		coords = points.split()
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		##Creates visualisation of gate and text file of gate info
		Ana.oval_gate(name, gate_name, coords[0], coords[1], coords[2], coords[3], coords[4], coords[5])
		## Save visualisation to cloud storage.
		Ana.save_vis(gate_name + '.png')
		## Saves info about gate to cloud storage
		Ana.save_info(gate_name + '.txt')
		## Saves gate as fcs file
		Ana.save_fcs(gate_name)
		## Clean up.
		os.remove(name)
		os.remove(gate_name + '.txt')
		os.remove(gate_name + '.png')
		os.remove(gate_name)
	elif (commands[0] == 'gate_poly'):
		name = commands[1]
		points = commands[2]
		gate_name = commands[3]
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		##Creates visualisation of gate and text file of gate info
		Ana.poly_gate(name, gate_name, points)
		## Save visualisation to cloud storage.
		Ana.save_vis(gate_name + '.png')
		## Saves info about gate to cloud storage
		Ana.save_info(gate_name + '.txt')
		## Saves gate as fcs file
		Ana.save_fcs(gate_name)
		## Clean up.
		os.remove(name)
		os.remove(gate_name + '.txt')
		os.remove(gate_name + '.png')
		os.remove(gate_name)
	elif (commands[0] == 'change_axis'):
		name = commands[1]
		x_axis = commands[2]
		y_axis = commands[3]
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		##Creates a visualisation of the graph with different axis
		Ana.change_axis(name, x_axis, y_axis)
		##Saves visualisation to loud storage
		Ana.save_vis(name + '1.png')
		## Clean up
		os.remove(name)
		os.remove(name + '1.png')
	# Delete any processed tasks from queue.
	if task_id is not None:
		Queue.delete('jobs', task_id)
