###########################################################################
## \file app/tools.py
## \brief Stores all the available tools and their actions
## \author mrudelle@keesaco.com of Keesaco
## \todo	Decouple permissions and authentication
###########################################################################

import API.APIQueue as queue
from django.core.urlresolvers import reverse
import API.APILogging as logging
import API.APIPermissions as ps
import API.APIDatastore as ds
import API.PALUsers as auth
from Permissions.Types import FileInfo, Permissions
from uuid import uuid1

DATA_BUCKET = '/fc-raw-data/'

###########################################################################
## \brief Is called when a gating is requested
## \param Dictionary gate_params - list of gating parameters
## \author mrudelle@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
## \todo Does this not want to be multiple tools?
## \todo Make quadrant and normal gating data gating not simple gating
###########################################################################
def simple_gating(gate_params):
	points = gate_params['points']
	reverse_gate = '0'

	if 'reverse' in gate_params:
		if (gate_params['reverse']):
			reverse_gate = '1'

	## Generate unique datastore path, ensuring uniqueness.
	while True:
		new_name = str(uuid1())
		new_path = ds.generate_path(DATA_BUCKET, None, new_name)
		if not ds.check_exists(new_path, None):
			break

	if (gate_params['tool'] == "rectangular_gating") :
		if len(points) == 4 :
			#Reoder the point to take the topLeft and bottomRight points of the square 
			if points[0] > points[2]:
				tempcoor = points[0]
				points[0] = points[2]
				points[2] = tempcoor
			if points[1] > points[3]:
				tempcoor = points[1]
				points[1] = points[3]
				points[3] = tempcoor

			gating_request = " ".join(str(p) for p in points)

			queue.gate_rectangle(gate_params['filename'], gating_request, new_name, reverse_gate, "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the rectangular gating was performed correctly", new_path, gate_params['filename'])
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " length:" + str(len(points)) + " is not equal to 4")

	elif (gate_params['tool'] == "polygon_gating") :
		if len(points)%2 == 0 :
			gating_request = " ".join(str(p) for p in points)

			queue.gate_polygon(gate_params['filename'], gating_request, new_name, reverse_gate, "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the polygonal gating was performed correctly", new_path, gate_params['filename'])
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(points))-1 + " is not pair")

	elif (gate_params['tool'] == "oval_gating") :
		if len(points) == 6 :
			gating_request = " ".join(str(p) for p in points)

			queue.gate_circle(gate_params['filename'], gating_request, new_name, reverse_gate, "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the oval gating was performed correctly", new_path, gate_params['filename'])
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(points)) + " is not even")

	elif (gate_params['tool'] == 'normal_gating') :
		if len(points) == 1 :
			gating_request = str(points[0])

			queue.gate_normal(gate_params['filename'], new_name, reverse_gate, "FSC-A", "SSC-A", gating_request);
			return generate_gating_feedback("success", "the normal gating was performed correctly", new_path, gate_params['filename'])
		else:
			return generate_gating_feedback("fail", "notcorrect, wrong number of arguments")

	elif (gate_params['tool'] == 'quadrant_gating') :
		if len(points) == 2 :
			other_new_names = []
			for i in range(0, 3):
				while True:
					next_new_name = str(uuid1())
					path = ds.generate_path(DATA_BUCKET, None, new_name)
					if not ds.check_exists(new_path, None):
						other_new_names.append(next_new_name)
						break
			x_coord = str(points[0])
			y_coord = str(points[1])
			queue.gate_quadrant(gate_params['filename'], x_coord, y_coord, new_name, other_new_names[0], other_new_names[1], other_new_names[2], "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the quadrant gate was performed correctly", new_path, gate_params['filename'])
		else:
			return generate_gating_feedback("fail", "notcorrect, wrong number of arguments")

	elif (gate_params['tool'] == 'kmeans_gating') :
		if len(points) == 1 :
			clusters = new_name
			number_gates = points[0]
			for i in range(0, number_gates):
				while True:
					next_new_name = str(uuid1())
					path = ds.generate_path(DATA_BUCKET, None, new_name)
					if not ds.check_exists(new_path, None):
						clusters = clusters + " " + next_new_name
						break
			queue.gate_kmeans(gate_params['filename'], clusters, str(number_gates), "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the kmeans gate was performed correctly", new_path, gate_params['filename'])
		else:
			return generate_gating_feedback("fail", "notcorrect, wrong number of arguments")

	else :
		return generate_gating_feedback("fail", "The gate " + gate_params['tool'] + " is not known")

###########################################################################
## \brief Is called when the requested tool is not in the dictionary of known tools
## \param Dictionary gate_params - list of gating parameters
## \return a dictionary with the status of the tool call
## \author mrudelle@keesaco.com of Keesaco
###########################################################################
def no_such_tool(gate_params):

	## \todo Do we really need to log the entire tool list? It's defined literally.
	logging.error('The tool "'+ gate_params['tool'] +'" is unknown. The known tools are: {' +
		', '.join(list(AVAILABLE_TOOLS.keys())) + '}' )
	return generate_gating_feedback("fail","The tool you selected is not reconized by the server", None)


## TODO the url should be a redirection in the future
###########################################################################
## \brief Generate a dictionary aimed to the client side in order to provide feedback on a gating operation
## \param status - Status of the operation, usualy success or fail
## \param message - more explanation on the status
## \param newgraphurl - url of the new graph
## \return a dictionary with the status of the tool call
## \author mrudelle@keesaco.com of Keesaco
## \author jmccrea@keesaco.com of Keesaco
## \note 	This is currently the method used to set permissions on gates
##			in future this should be refactored. Perhaps providing a base
##			tool class to inherit from
## \todo	Move permissions code out of here
###########################################################################
def generate_gating_feedback(status, message, new_graph_name = None, existing_name = None):
	if new_graph_name is not None:
		## Authenticate and get user 
		authed_user = auth.get_current_user()
		user_key = ps.get_user_key_by_id(authed_user.user_id())

		## Get previous file permissions.
		previous_file = ps.get_file_by_name(DATA_BUCKET + existing_name)
		previous_permissions = ps.get_user_file_permissions(previous_file.key, user_key)

		## Add permissions to new file.
		new_file = FileInfo(file_name = new_graph_name,
							owner_key = user_key,
							friendly_name = previous_file.friendly_name + '-gate')
		file_key = ps.add_file(new_file)
		ps.add_file_permissions(file_key,
								user_key,
								Permissions (
									previous_permissions.read,
									previous_permissions.write,
									previous_permissions.full_control
								),
								previous_permissions.colour,
								False)

	return {
		'status': status,
		'message': message,
		'url': reverse('get_graph', args=[new_graph_name]),
		'graphName' : new_graph_name
	}

AVAILABLE_TOOLS = {
	'oval_gating' 			: simple_gating,
	'rectangular_gating'	: simple_gating,
	'polygon_gating'		: simple_gating,
	'normal_gating'			: simple_gating,
	'quadrant_gating'		: simple_gating,
	'kmeans_gating'			: simple_gating
}
