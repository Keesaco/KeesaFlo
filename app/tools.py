import API.APIQueue as queue
from django.core.urlresolvers import reverse

###########################################################################
## \brief Is called when a rectangular gating is requested.
## \param params - Paramesters of this gating, string of the form: topLeftx,topLefty,bottomRightx,bottomRighty,newFilename
## \return a dictionary with the status of the gating, a short message and the link to the newly created graph
###########################################################################
def rect_gating(paramList):
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

		return {
				'status': "success",
				'message': "the rectangular gating was performed correctly",
				'url': reverse('get_graph', args=[newName])
			}
	else:
		return {
				'status': "fail",
				'message': "notcorrect " + params + " length:" + str(len(paramList)) + " is not equal to 4",
				'url': None
			}

###########################################################################
## \brief Is called when a polygonal gating is requested.
## \param params - Paramesters of this gating, string of the form: x1,y1,x2,y2,...xn,yn,newFilename
## \return a dictionary with the status of the gating, a short message and the link to the newly created graph
###########################################################################
def poly_gating(paramList):
	if len(paramList)%2 == 1 :
		gatingRequest = " ".join(paramList[0:-1])        

		newName = paramList[-1] + "-polyGate";
		queue.gate_polygon(paramList[-1], gatingRequest, newName, "0", "FSC-A", "PE-A");

		return {
				'status': "success",
				'message': "the polygonal gating was performed correctly",
				'url': reverse('get_graph', args=[newName])
			}
	else:
		return {
				'status': "fail",
				'message': "notcorrect " + params + " #pointCoordinates:" + str(len(paramList))-1 + " is not pair",
				'url': None
			}

###########################################################################
## \brief Is called when an oval gating is requested.
## \param params - Paramesters of this gating, string of the form: meanx,meany,point1x,point1y,point2x,point2y,newFilename
## \return a dictionary with the status of the gating, a short message and the link to the newly created graph
###########################################################################
def oval_gating(paramList):
	if len(paramList) == 7 :
		gatingRequest = " ".join(paramList[0:-1])        

		newName = paramList[-1] + "-ovalGate";
		queue.gate_circle(paramList[-1], gatingRequest, newName, "0", "FSC-A", "PE-A");

		return {
				'status': "success",
				'message': "the oval gating was performed correctly",
				'url': reverse('get_graph', args=[newName])
			}
	else:
		return {
				'status': "fail",
				'message': "notcorrect " + params + " #pointCoordinates:" + str(len(paramList)) + " is not even",
				'url': None
			}

###########################################################################
## \brief Is called when the requested tool is not in the dictionary of known tools
## \param paramsList - Paramesters that comes with this tool call
## \return a dictionary with the status of the tool call
###########################################################################
def no_such_tool(paramList):
	return {
			'status': "fail",
			'message': "The tool you selected is not reconized by the server",
			'url': None
		}

AVAILABLE_TOOLS = {
	'rectangular_gating' : rect_gating,
	'polygon_gating' : poly_gating,
	'oval_gating' : oval_gating
}
