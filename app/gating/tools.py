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
## \param Dictionary params - list of gating parameters
## \author mrudelle@keesaco.com of Keesaco
## \todo Does this not want to be multiple tools?
###########################################################################
def simple_gating(gateParams):
	points = gateParams['points']

	if (gateParams['tool'] == "rectangular_gating") :
		if len(points) == 5 :
			#Reoder the point to take the topLeft and bottomRight points of the square 
			if points[0] > points[2]:
				tempcoor = points[0]
				points[0] = points[2]
				points[2] = tempcoor
			if points[1] > points[3]:
				tempcoor = points[1]
				points[1] = points[3]
				points[3] = tempcoor

			gatingRequest =" ".join(points)

			newName = gateParams['filename'] + "-rectGate";
			queue.gate_rectangle(gateParams['filename'], gatingRequest, newName, "1", "FSC-A", "PE-A");
			return generate_gating_feedback("success", "the rectangular gating was performed correctly", reverse('get_graph', args=[newName]))
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " length:" + str(len(points)) + " is not equal to 4")

	elif (gateParams['tool'] == "polygon_gating") :
		if len(points)%2 == 0 :
			gatingRequest = " ".join(points)

			newName = gateParams['filename'] + "-polyGate";
			queue.gate_polygon(gateParams['filename'], gatingRequest, newName, "0", "FSC-A", "PE-A");
			return generate_gating_feedback("success", "the polygonal gating was performed correctly", reverse('get_graph', args=[newName]))
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(points))-1 + " is not pair")

	elif (gateParams['tool'] == "oval_gating") :
		if len(points) == 6 :
			gatingRequest = " ".join(points)

			newName = gateParams['filename'] + "-ovalGate";
			queue.gate_circle(gateParams['filename'], gatingRequest, newName, "0", "FSC-A", "PE-A");
			return generate_gating_feedback("success", "the oval gating was performed correctly", reverse('get_graph', args=[newName]))
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(points)) + " is not even")
		
	else :
		return generate_gating_feedback("fail", "The gate " + gateParams['tool'] + " is not known")

###########################################################################
## \brief Is called when the requested tool is not in the dictionary of known tools
## \param Dictionary params - list of gating parameters
## \return a dictionary with the status of the tool call
## \author mrudelle@keesaco.com of Keesaco
###########################################################################
def no_such_tool(params):

	## \todo Do we really need to log the entire tool list? It's defined literally.
	logging.error('The tool "'+ params['tool'] +'" is unknown. The known tools are: {' +
		', '.join(list(AVAILABLE_TOOLS.keys())) + '}' )
	return generate_gating_feedback("fail","The tool you selected is not reconized by the server")


## TODO the url should be a redirection in the future
###########################################################################
## \brief Generate a dictionary aimed to the client side in order to provide feedback on a gating operation
## \param status - Status of the operation, usualy success or fail
## \param message - more explanation on the status
## \param newgraphurl - url of the new graph
## \return a dictionary with the status of the tool call
## \author mrudelle@keesaco.com of Keesaco
###########################################################################
def generate_gating_feedback(status, message, newgraphurl = None):
	return {
		'status': status,
		'message': message,
		'url': newgraphurl
	}

AVAILABLE_TOOLS = {
	'gating' : simple_gating
}
