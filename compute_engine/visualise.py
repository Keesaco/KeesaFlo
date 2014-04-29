###########################################################################
## \file compute_engine/visualise.py
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
## \author rmurley@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.visualise
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Should be called by the Compute Engine startup sheel script. Depends on AnalysisAPI.
###########################################################################
import os, time, sys
import API.APIAnalysis as Ana
import API.APIQueue as Queue

def gate_clean_up(gate_name):
	os.remove(gate_name + '.png')
	os.remove(gate_name + '.txt')
	os.remove(gate_name)

def save_gate(gate_name):
	## Saves visualisation of gate to cloud storage
	Ana.save_vis(gate_name + '.png')
	## Saves info about gate to cloud storage
	Ana.save_info(gate_name + '.txt')
	## Saves gate as fcs file
	Ana.save_fcs(gate_name)

def shape_gating(commands):
	name = commands[1]
	points = commands[2]
	gate_name = commands[3]
	reverse = commands[4]
	x_axis = commands[5]
	y_axis = commands[6]
	coords = points.split()
	##Loads raw fcs data from cloud storage
	Ana.load_fcs(name)
	##Creates visualisation of gate and text file of gate info
	if(commands[0] == 'gate_rec'):
		exitcode = Ana.rect_gate(name, gate_name, coords[0], coords[1], coords[2], 
			coords[3], reverse, x_axis, y_axis)
	elif(commands[0] == 'gate_cir'):
		exitcode = Ana.oval_gate(name, gate_name, coords[0], coords[1], coords[2], 
			coords[3], coords[4], coords[5], reverse, x_axis, y_axis)
	elif(commands[0] == 'gate_poly'):
		exitcode = Ana.poly_gate(name, gate_name, points, reverse, x_axis, y_axis)
	elif(commands[0] == 'gate_bool'):
		exitcode = Ana.bool_gate(name, gate_name, commands[7], commands[8], points, reverse, commands[9], 
			commands[10], commands[11], x_axis, y_axis, commands[12], commands[13])
	if(exitcode == 0):
		## Save visualisation to cloud storage.
		save_gate(gate_name)
		## Clean up.
		gate_clean_up(gate_name)
		os.remove(name)
	return True

def axis_change(commands):
	name = commands[1]
	x_axis = commands[2]
	y_axis = commands[3]
	##Loads raw fcs data from cloud storage
	Ana.load_fcs(name)
	##Creates a visualisation of the graph with different axis
	exitcode = Ana.change_axis(name, x_axis, y_axis)
	if(exitcode == 0):
		##Saves visualisation to cloud storage
		Ana.save_vis(name + x_axis + y_axis + '.png')
		## Clean up
		os.remove(name)
		os.remove(name + x_axis + y_axis + '.png')
	return True

def visualise(commands):
	# Get name.
	name = commands[1]
	## Load raw fcs data from cloud storage.
	Ana.load_fcs(name)
	## Create visualisation of raw fcs data.
	exitcode = Ana.visualise(name)
	if(exitcode == 0):
		## Save visualisation to cloud storage.
		Ana.save_vis(name + '.png')
		## Saves info about fcs file to cloud storage
		Ana.save_info(name + 'info.txt')
		Ana.save_info(name + '.txt')
		## Clean up.
		os.remove(name)
		os.remove(name + '.png')
		os.remove(name + '.txt')
		os.remove(name + 'info.txt')
	return True

def change_plot(commands):
	name = commands[1]
	plot_name = commands[4]
	##Load raw fcs data from cloud storage
	Ana.load_fcs(name)
	##Create visualisation of graph with different plot type
	if(commands[0] == 'dot_plot'):
		exitcode = Ana.dot_plot(name, plot_name, commands[2], commands[3])
	elif(commands[0] == 'contour_plot'):
		exitcode = Ana.contour_plot(name, plot_name, commands[2], commands[3])
	if(exitcode == 0):
		## Saves visualisation to cloud storage
		Ana.save_vis(plot_name)
		## Clean up
		os.remove(name)
		os.remove(plot_name)
	return True

def data_gate(commands):
	if(commands[0] == 'gate_norm'):
		name = commands[1]
		gate_name = commands[2]
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		##Creates visualisation of gate and text file of gate info
		exitcode = Ana.norm_gate(name, gate_name, commands[3], commands[4], commands[5], commands[6])
		if(exitcode == 0):
			save_gate(gate_name)
			## Clean up.
			gate_clean_up(gate_name)
			os.remove(name)
	elif(commands[0] == 'gate_kmeans'):
		name = commands[1]
		cluster_names = commands[2]
		number_clusters = commands[3]
		x_axis = commands[4]
		y_axis = commands[5]
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		## Creates visualisation and .fcs file of gate
		exitcode = Ana.kmeans_gate(name, cluster_names, number_clusters, x_axis, y_axis)
		number = int(number_clusters)
		names = cluster_names.split(" ")
		if(exitcode == 0):
			for i in range(0, number):
				current_gate_name = names[i]
				## Saves visualisation of gate to cloud storage
				save_gate(current_gate_name)
				## Clean up
				gate_clean_up(current_gate_name)
			os.remove(name)
	return True

def quadrant_gate(commands):
	name = commands[1]
	##Loads raw fcs data from cloud storage
	Ana.load_fcs(name)
	## Creates visualisation and .fcs file of gate
	exitcode = Ana.quad_gate(name, commands[2], commands[3], commands[4], commands[5], commands[6], commands[7], commands[8], commands[9])
	if(exitcode == 0):
		for i in range(4, 8):
			current_gate_name = commands[i]
			save_gate(current_gate_name)
			## Clean up
			gate_clean_up(current_gate_name)
		os.remove(name)
	return True

def kill(commands):
	return False

AVAILABLE_TASKS = {
	'kill'			: kill,
	'vis'			: visualise,
	'gate_rec'		: shape_gating,
	'gate_cir'		: shape_gating,
	'gate_poly'		: shape_gating,
	'gate_bool'		: shape_gating,
	'change_axis'	: axis_change,
	'dot_plot'		: change_plot,
	'contour_plot'	: change_plot,
	'gate_quad'		: quadrant_gate,
	'gate_norm'		: data_gate,
	'gate_kmeans'	: data_gate
}

# Check task queue until 'kill' command is received.
alive = True
while alive:
	# Lease a command.
	try:
		task = Queue.lease('jobs', 30)
	except Exception, e:
		print e
	# If there are tasks in queue extract id and commands, else restart loop and check queue again.
	if task is not None:
		task_id = task[0]
		commands = task[1]
	else:
		time.sleep(0.9)
		continue
	functionToCall = AVAILABLE_TASKS[commands[0]]
	alive = functionToCall(commands)
	# Delete any processed tasks from queue.
	if task_id is not None:
		Queue.delete('jobs', task_id)