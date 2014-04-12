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
## \param paramsList - Paramesters that comes with this gating tool call
## \param name - name of the tool that triggered this call
## \return a dictionary with the status of the tool call
## \author mrudelle@keesaco.com of Keesaco
###########################################################################
def simple_gating(paramList, name):
	gateName = paramList.pop(0);

	if (gateName == "rectangular_gating") :
		if len(paramList) == 5 :
			#Reoder the point to take the topLeft and bottomRight points of the square 
			if paramList[0] > paramList[2]:
				tempcoor = paramList[0]
				paramList[0] = paramList[2]
				paramList[2] = tempcoor
			if paramList[1] > paramList[3]:
				tempcoor = paramList[1]
				paramList[1] = paramList[3]
				paramList[3] = tempcoor

			gatingRequest =" ".join(paramList[0:4])

			newName = paramList[-1] + "-rectGate";
			queue.gate_rectangle(paramList[-1], gatingRequest, newName, "1", "FSC-A", "PE-A");
			return generate_gating_feedback("success", "the rectangular gating was performed correctly", reverse('get_graph', args=[newName]))
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " length:" + str(len(paramList)) + " is not equal to 4", None)

	elif (gateName == "polygon_gating") :
		if len(paramList)%2 == 1 :
			gatingRequest = " ".join(paramList[0:-1])        

			newName = paramList[-1] + "-polyGate";
			queue.gate_polygon(paramList[-1], gatingRequest, newName, "0", "FSC-A", "PE-A");
			return generate_gating_feedback("success", "the polygonal gating was performed correctly", reverse('get_graph', args=[newName]))
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(paramList))-1 + " is not pair", None)

	elif (gateName == "oval_gating") :
		if len(paramList) == 7 :
			gatingRequest = " ".join(paramList[0:-1])        

			newName = paramList[-1] + "-ovalGate";
			queue.gate_circle(paramList[-1], gatingRequest, newName, "0", "FSC-A", "PE-A");
			return generate_gating_feedback("success", "the oval gating was performed correctly", reverse('get_graph', args=[newName]))
		else:
			return generate_gating_feedback("fail", "notcorrect " + params + " #pointCoordinates:" + str(len(paramList)) + " is not even", None)
		
	else :
		return generate_gating_feedback("fail", "The gate "+gateName+" is not known", None)

###########################################################################
## \brief Is called when the requested tool is not in the dictionary of known tools
## \param paramsList - Paramesters that comes with this tool call
## \return a dictionary with the status of the tool call
## \author mrudelle@keesaco.com of Keesaco
###########################################################################
def no_such_tool(paramList, name):

	logging.error('The tool "'+ name +'" is unknown. The known tools are: {' + 
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
def generate_gating_feedback(status, message, newgraphurl):
	return {
		'status': status,
		'message': message,
		'url': newgraphurl
	}

AVAILABLE_TOOLS = {
	'gating' : simple_gating
}
