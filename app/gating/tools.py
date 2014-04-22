###########################################################################
## \file app/tools.py
## \brief Stores all the available tools and their actions
## \author mrudelle@keesaco.com of Keesaco
###########################################################################

import API.APIQueue as queue
from django.core.urlresolvers import reverse
import API.APILogging as logging

###########################################################################
## \brief Is called when a gating is requested
## \param Dictionary gate_params - list of gating parameters
## \author mrudelle@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
## \todo Does this not want to be multiple tools?
###########################################################################
def simple_gating(gate_params):
	points = gate_params['points']
	reverse_gate = '0'
	
	if 'reverse' in gate_params:
		if (gate_params['reverse']):
			reverse_gate = '1'

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

			new_name = gate_params['filename'] + "-rectGate";
			queue.gate_rectangle(gate_params['filename'], gating_request, new_name, reverse_gate, "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the rectangular gating was performed correctly", new_name)
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " length:" + str(len(points)) + " is not equal to 4")

	elif (gate_params['tool'] == "polygon_gating") :
		if len(points)%2 == 0 :
			gating_request = " ".join(str(p) for p in points)

			new_name = gate_params['filename'] + "-polyGate";
			queue.gate_polygon(gate_params['filename'], gating_request, new_name, reverse_gate, "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the polygonal gating was performed correctly", new_name)
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(points))-1 + " is not pair")

	elif (gate_params['tool'] == "oval_gating") :
		if len(points) == 6 :
			gating_request = " ".join(str(p) for p in points)

			new_name = gate_params['filename'] + "-ovalGate";
			queue.gate_circle(gate_params['filename'], gating_request, new_name, reverse_gate, "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the oval gating was performed correctly", new_name)
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(points)) + " is not even")

	elif (gate_params['tool'] == 'normal_gating') :
		if len(points) == 1 :
			gating_request = str(points[0])

			new_name = gate_params['filename'] + "-normGate";
			queue.gate_normal(gate_params['filename'], new_name, reverse_gate, "FSC-A", "SSC-A", gating_request);
			return generate_gating_feedback("success", "the normal gating was performed correctly", new_name)
		else:
			return generate_gating_feedback("fail", "notcorrect, wrong number of arguments")

	elif (gate_params['tool'] == 'quadrant_gating') :
		if len(points) == 2 :
			new_name = []
			for i in range(0, 4):
				new_name.append(gate_params['filename'] + "-quad" + str(i) + "Gate")
			x_coord = str(points[0])
			y_coord = str(points[1])
			queue.gate_quadrant(gate_params['filename'], x_coord, y_coord, new_name[0], new_name[1], new_name[2], new_name[3], "FSC-A", "SSC-A");
			return generate_gating_feedback("success", "the quadrant gate was performed correctly", new_name[0])
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
###########################################################################
def generate_gating_feedback(status, message, new_graph_name = None):
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
	'quadrant_gating'		: simple_gating
}
