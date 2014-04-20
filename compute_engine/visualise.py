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
		exitcode = Ana.visualise(name)
		if(exitcode == 0):
			## Save visualisation to cloud storage.
			Ana.save_vis(name + '.png')
			## Saves info about fcs file to cloud storage
			Ana.save_info(name + 'info.txt')
			## Clean up.
			os.remove(name)
			os.remove(name + '.png')
			os.remove(name + 'info.txt')
	elif (commands[0] == 'gate_rec' or commands[0] == 'gate_cir' or commands[0] == 'gate_poly' or 
		commands[0] == 'gate_bool'):
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
			Ana.save_vis(gate_name + '.png')
			## Converts info file from .txt to .html
			f = open(gate_name + '.txt', 'r')
			info = f.readline()
			f.close()
			stats = info.split()
			f2 = open(gate_name + '.html', 'w')
			f2.write('<link href="{static "css/app.css" %}" rel ="stylesheet"')
			f2.write('<p>Number of cells in gate: <span class="gating_num">' + stats[0] + '</span></p>')
			f2.write('<p>Number of cells in total: <span class="gating_num">' + stats[1] + '</span></p>')
			f2.write('<p>Percentage ratio: <span class="gating_num">' + str(float(stats[2])*100) + '%</span></p>')
			f2.close()
			## Saves info about gate to cloud storage
			Ana.save_info(gate_name + '.html')
			## Saves gate as fcs file
			Ana.save_fcs(gate_name)
			## Clean up.
			os.remove(gate_name + '.txt')
			os.remove(gate_name + '.png')
			os.remove(gate_name)
			os.remove(name)
	elif (commands[0] == 'change_axis'):
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
	elif (commands[0] == 'dot_plot' or commands[0] == 'contour_plot'):
		name = commands[1]
		x_axis = commands[2]
		y_axis = commands[3]
		plot_name = commands[4]
		##Load raw fcs data from cloud storage
		Ana.load_fcs(name)
		##Create visualisation of graph with different plot type
		if(commands[0] == 'dot_plot'):
			exitcode = Ana.dot_plot(name, plot_name, x_axis, y_axis)
		elif(commands[0] == 'contour_plot'):
			exitcode = Ana.contour_plot(name, plot_name, x_axis, y_axis)
		if(exitcode == 0):
			## Saves visualisation to cloud storage
			Ana.save_vis(plot_name)
			## Clean up
			os.remove(name)
			os.remove(plot_name)
	elif (commands[0] == 'gate_norm'):
		name = commands[1]
		gate_name = commands[2]
		reverse = commands[3]
		x_axis = commands[4]
		y_axis = commands[5]
		scale_factor = commands[6]
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		##Creates visualisation of gate and text file of gate info
		exitcode = Ana.norm_gate(name, gate_name, reverse, x_axis, y_axis, scale_factor)
		if(exitcode == 0):
			## Saves visualisation of gate to cloud storage
			Ana.save_vis(gate_name + '.png')
			## Saves info about gate to cloud storage
			Ana.save_info(gate_name + '.txt')
			## Saves gate as fcs file
			Ana.save_fcs(gate_name)
			## Clean up.
			os.remove(gate_name + '.txt')
			os.remove(gate_name + '.png')
			os.remove(gate_name)
			os.remove(name)
	elif (commands[0] == 'gate_quad'):
		name = commands[1]
		x_coord = commands[2]
		y_coord = commands[3]
		x_axis = commands[8]
		y_axis = commands[9]
		##Loads raw fcs data from cloud storage
		Ana.load_fcs(name)
		## Creates visualisation and .fcs file of gate
		exitcode = 0;
		Ana.quad_gate(name, x_coord, y_coord, commands[4], commands[5], commands[6], commands[7], x_axis, y_axis)
		if(exitcode == 0):
			for i in range(4, 8):
				current_gate_name = commands[i]
				## Saves visualisation of gate to cloud storage
				Ana.save_vis(current_gate_name + '.png')
				## Saves info about gate to cloud storage
				Ana.save_info(current_gate_name + '.txt')
				## Saves gate as fcs file
				Ana.save_fcs(current_gate_name)
				## Clean up
				os.remove(current_gate_name + '.png')
				os.remove(current_gate_name + '.txt')
				os.remove(current_gate_name)
			os.remove(name)
	# Delete any processed tasks from queue.
	if task_id is not None:
		Queue.delete('jobs', task_id)
