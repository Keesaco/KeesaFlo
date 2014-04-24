/**
 * \file app/static/js/graphTools.js
 * \brief JavaScript library to manage graph related tools
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 */
/**
 * \package app.static.js.graphTools
 * \brief Provides methods for triggering tool event
 */

/**
 * ksfTools constructor used for namespace
 * \author mrudelle@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfGraphTools()
{

}

FEEDBACK_SUCCESS = "alert-success";
FEEDBACK_INFO = "alert-info";
FEEDBACK_WARING = "alert-warning";
FEEDBACK_DANGER = "alert-danger";

ANALYSIS_STATUS_URI = '/app/data/json/analysis_status/';
FILE_VIEW_HASH		= '#!/preview/';
GATING_URI		= "/app/gating/tools/";

/**
 *	Milliseconds between requests for new graphs
 */
GRAPH_POLL_INTERVAL = 1000;

/**
 *	Number of times to attempt to get a new graph before giving up and requiring a manual refresh
 */
GRAPH_LOAD_MAX_ATTEMPTS = 20;

ksfGraphTools.timeoutCounter = GRAPH_LOAD_MAX_ATTEMPTS;

/*
	Each of the folowing elements represent a graph related tool
	they contains - an ELEMENT_ID that allows one to access the tool's button
				  - a function onGraphClick, trigered by a click on the graph when this tool is selected
				  - a function resetTool, called when the tool is unselected
				  - a function onGraphMouseMove, called to redraw the canvas when the mouse is moving over it
				  - a function requestGating which ask the server to perform a gating on the dataset.
				  - some personal variables related to the behaviour of the tool
				  */

// This tool propose to draw a rectangle in two clicks, get the coordinates (relative to the image) of the rectangle.
// A third click reset the selection
ksfGraphTools.RectangularGating = {
	startx : null,
	starty : null,
	endx : null,
	endy : null,

	ELEMENT_ID : "#tool_rectangular_gating",

	onGraphClick : function(event)
	{
		var posX = event.pageX - $(GRAPH_ID).offset().left,
		posY = event.pageY - $(GRAPH_ID).offset().top;

		if ((this.startx === null) || (this.starty === null))
		{
			this.startx = posX;
			this.starty = posY;
			ksfCanvas.toolText("You just started with the rectangle tool " + (posX) + ' , ' + (posY));
		}
		else if ((this.endx === null) || (this.endy === null))
		{
			this.endx = posX;
			this.endy = posY;
			ksfCanvas.drawBox(this.startx, this.starty, this.endx-this.startx, this.endy-this.starty, 1);
			ksfCanvas.toolText("You just finished with the rectangle tool [" + "(" + this.startx + "," + this.starty + ")"  + ' , ' + "(" + this.endx + "," + this.endy + ")" + ']');
			ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
		}
		else
		{
			this.resetTool();
			ksfCanvas.clear();
			ksfCanvas.toolText("The rectangle has been reset.");
		}
	},

	onGraphMouseMove : function(event)
	{
		var posX = event.pageX - $(GRAPH_ID).offset().left,
		posY = event.pageY - $(GRAPH_ID).offset().top;
		if (   ( (this.endx === null)   || (this.endy === null) )
			&& ( (this.startx !== null) || (this.starty !== null) ) )
		{
			ksfCanvas.drawBox(this.startx, this.starty, posX-this.startx, posY-this.starty, 0.5);
		}
	},

	resetTool : function()
	{
		this.starty = null;
		this.startx = null;
		this.endy = null;
		this.endx = null;
		ksfCanvas.clear();
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
	},
	
	requestGating : function()
	{
		ksfGraphTools.sendGatingRequest('rectangular_gating', [this.startx, this.starty, this.endx, this.endy]);
	}
}

// This tool propose to draw a polygon, the polygon is closed whenever
// ones select a point too close from another or if the new edge cross one of the previous one.
ksfGraphTools.PolygonGating = {

	PointList : [],
	xList : [],
	yList : [],
	SelectionDone : false,
	ELEMENT_ID : "#tool_polygon_gating",
	START_RADIUS : 10,

	onGraphClick : function(event)
	{
		if (this.SelectionDone)
		{
			return;
		}
		
		var posX, posY, x, y, d;

		posX = event.pageX - $(GRAPH_ID).offset().left;
		posY = event.pageY - $(GRAPH_ID).offset().top;

		// Triggered when the path is closed
		if (this.distanceToStart(posX, posY) < this.START_RADIUS)
		{
			ksfCanvas.drawPolygon(this.xList, this.yList, this.xList[0], this.yList[0], this.START_RADIUS);
			this.SelectionDone = true;
			ksfCanvas.toolText("Selection is finished: "+ (this.xList.length) + " points");
			ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
		}
		else
		{
			this.xList.push(posX);
			this.yList.push(posY);
			ksfCanvas.drawPolygon(this.xList, this.yList, null, null, this.START_RADIUS);
			ksfCanvas.toolText("point #"+ (this.xList.lengt) +": ("+posX+","+posY+")");
		}
	},

	resetTool : function()
	{
		this.xList = [];
		this.yList = [];
		this.SelectionDone = false;
		ksfCanvas.clear();
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
	},

	onGraphMouseMove : function(event)
	{
		ksfCanvas.setCursor('crosshair');
		if (this.SelectionDone)
		{
			ksfCanvas.drawPolygon(this.xList, this.yList, this.xList[0], this.yList[0], this.START_RADIUS);
			ksfCanvas.toolText("selection is finished: "+ (this.xList.length) + "points");
		}
		else
		{
			var posX = event.pageX - $(GRAPH_ID).offset().left,
			posY = event.pageY - $(GRAPH_ID).offset().top;
			ksfCanvas.drawPolygon(this.xList, this.yList, posX, posY, this.START_RADIUS);
			if (this.distanceToStart(posX, posY) < this.START_RADIUS)
			{
				ksfCanvas.setCursor('pointer');
			}
		}
	},

	//return the distance to the starting point
	distanceToStart : function(posx, posy)
	{
		var x, y;
		if (this.xList.length >= 1)
		{
			x = this.xList[0]-posx;
			y = this.yList[0]-posy;
			return Math.sqrt(Math.pow(x,2)+Math.pow(y,2));
		}
		return Math.MAX;
	},

	requestGating : function()
	{
		ksfGraphTools.sendGatingRequest('polygon_gating', this.xList.concat(this.yList));
	}
}

//This tool allows one to create an oval shaped selection
//you have to select the central point, then the smaller radius and finally the orientation and the biggest radius.
ksfGraphTools.OvalGating = {
	params : null,
	
	centerx : null, 
	centery : null, 
	r1 : null, 
	pointx : null, 
	pointy : null, 

	ELEMENT_ID : "#tool_oval_gating",

	onGraphClick : function(event)
	{
		var posX = event.pageX - $(GRAPH_ID).offset().left,
		posY = event.pageY - $(GRAPH_ID).offset().top;
		
		if (this.centerx === null || this.centery === null)
		{
			this.centerx = posX;
			this.centery = posY;
			ksfCanvas.toolText("Select the smaller radius");
		}
		else if (this.r1 === null)
		{
			this.r1 = Math.sqrt(Math.pow(this.centerx-posX,2)+Math.pow(this.centery-posY,2));
			ksfCanvas.toolText("Select the oval\'s last point")
		}
		else if (this.pointx === null || this.pointy === null)
		{
			this.pointx = posX;
			this.pointy = posY;
			ksfCanvas.drawOval(this.centerx, this.centery, this.r1, this.pointx, this.pointy);
			ksfCanvas.toolText("Oval correctly selected");
			ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
		}
		else
		{
			this.resetTool();
			ksfCanvas.toolText("Select oval\'s center");
		}
		
	},

	onGraphMouseMove : function(event)
	{
		var posX = event.pageX - $(GRAPH_ID).offset().left,
		posY = event.pageY - $(GRAPH_ID).offset().top;

		if (this.centerx !== null || this.centery !== null)
		{
			if (this.r1 === null)
			{
				var r = Math.sqrt(Math.pow(this.centerx-posX,2)+Math.pow(this.centery-posY,2));
				ksfCanvas.drawCircle(this.centerx, this.centery, posX, posY);
			}
			else if (this.pointx === null || this.pointy === null)
			{
				ksfCanvas.drawOval(this.centerx, this.centery, this.r1, posX, posY);
			} 
		}
	},

	resetTool : function()
	{
		this.centerx = null; 
		this.centery = null; 
		this.r1 = null; 
		this.pointx = null; 
		this.pointy = null; 
		ksfCanvas.clear();
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
	},

	requestGating : function()
	{
		var tx = this.centerx-this.pointx,
			ty = this.centery-this.pointy;
		var angle = ksfGraphTools.mesureAngle(tx, ty);
		var p1x=this.centerx+Math.cos(angle-Math.PI/2)*this.r1,
		p1y=this.centery+Math.sin(angle-Math.PI/2)*this.r1;
		ksfGraphTools.sendGatingRequest('oval_gating',
										[this.centerx, this.centery, p1x, p1y, this.pointx, this.pointy] );
	}
}

//Sends a request for normal gating
ksfGraphTools.NormalGating = {
	scale_factor : null,

	ELEMENT_ID : "#tool_normal_gating",

	onGraphClick : function(event)
	{
	},

	onGraphMouseMove : function(event)
	{
	},

	resetTool : function()
	{
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
		this.scale_factor = 1;
	},

	requestGating : function()
	{
		ksfGraphTools.sendGatingRequest('normal_gating', [this.scale_factor]);
	}
}

//Sends a request for kmeans gating
ksfGraphTools.KmeansGating = {
	no_clusters : null,

	ELEMENT_ID : "#tool_kmeans_gating",

	onGraphClick : function(event)
	{
	},

	onGraphMouseMove : function(event)
	{
	},

	resetTool : function()
	{
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
		this.no_clusters = 3;
	},

	requestGating : function()
	{
		ksfGraphTools.sendGatingRequest('kmeans_gating', [this.no_clusters]);
	}
}

//Sends request for quadrant gating and draws cross displaying segmentation
ksfGraphTools.QuadrantGating = {
	centre_x : null,
	centre_y : null,

	ELEMENT_ID : "#tool_quadrant_gating",

	onGraphClick : function(event)
	{
		var posX = event.pageX - $(GRAPH_ID).offset().left,
		posY = event.pageY - $(GRAPH_ID).offset().top;

		if ((this.centre_x === null) || (this.centre_y === null))
		{
			this.centre_x = posX;
			this.centre_y = posY;
			ksfCanvas.toolText("You just selected a centre for the quadrant tool: " + (posX) + ' , ' + (posY));
			ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
		}
		else
		{
			this.resetTool();
			ksfCanvas.toolText("The quandrant tool has been reset.");
		}
	},

	onGraphMouseMove : function(event)
	{
		var posX = event.pageX - $(GRAPH_ID).offset().left,
		posY = event.pageY - $(GRAPH_ID).offset().top;
		if((this.centre_x === null) || (this.centre_y === null))
		{
			ksfCanvas.drawCross(posX, posY);
		}
	},

	resetTool : function()
	{
		this.centre_x = null; 
		this.centre_y = null; 
		ksfCanvas.clear();
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
	},

	requestGating : function()
	{
		ksfGraphTools.sendGatingRequest('quadrant_gating', [this.centre_x, this.centre_y]);
	}
}

/**
 * Perform a gating request and update the view correspondingly
 * \param String toolName - name of tool to use for gate
 * \param [Int] gatePoints - list of points which form the gate
 * \param Object params - Object with other gating parameters - this is used to extend the gating request object before the gating request is sent
 * \author mrudelle@keesaco.com of Keesaco
 * \note This might be moved to views.js in the future //JPM - might it?
 * \note deep-extend is not used for params
 */
function ksfGraphTools_sendGatingRequest(toolName, gatePoints, params)
{
	// allows to fetch the name correctly. In the future (final release) this should be replace by a json file fetched from the server containing all the file's data

	var currentFile = $("#scrapename").text().trim();

	var reverseGate = $('#chk_reverse_gate').first().is(':checked');
	
	ksfTools.CurrentTool.resetTool();
	ksfCanvas.toolText("Loading graph...");

	var gateReq = {
		tool 		: toolName,
		points 		: gatePoints,
		filename	: currentFile,
		reverse		: reverseGate
	};

	if (params)
	{
		$.extend(gateReq, params);
	}

	ksfReq.postJSON(GATING_URI, gateReq,
			function(response)
			{
				var feedbackType;
				switch (response.status)
				{
					case "success":
						feedbackType = FEEDBACK_SUCCESS;
						break;
					
					case "fail":
						feedbackType = FEEDBACK_DANGER;
						break;
					default:
						feedbackType = FEEDBACK_INFO;
				}
				ksfGraphTools.showFeedback(feedbackType, response.status, response.message);
				ksfCanvas.toolText("");
				setTimeout(ksfGraphTools.setGraphUrl(response.url, response.graphName), GRAPH_POLL_INTERVAL);
			},
			function(jqxhr, textStatus, error)
			{
				ksfGraphTools.showFeedback(FEEDBACK_DANGER, textStatus, error);
			} );
}
ksfGraphTools.sendGatingRequest = ksfGraphTools_sendGatingRequest;

/**
 * Change properly the graph image
 * \param url - [String] url of the new graph
 * \param String newFilename - file path of new gate
 * \param Int numRetries - the number of times to check the status of the gate before giving up. If undefined defaults to GRAPH_LOAD_MAX_ATTEMPTS.
 * \author jmccrea@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 * \note If the link throw an error it will enter a loop to reload the image
 */
function ksfGraphTools_setGraphUrl(url, newFilename, numRetries)
{
	// we let 20 sec for the graph to appear
	ksfGraphTools.timeoutCounter = typeof numRetries == 'undefined' ? GRAPH_LOAD_MAX_ATTEMPTS : numRetries;

	var gate_req = { filename : newFilename };
	var gateRedirect = newFilename.split('/')[2];
	ksfCanvas.setLoading(true);
	
	var gate_status = ksfReq.postJSON(ANALYSIS_STATUS_URI, gate_req,
		function(response)
		{
			if (response.error)
			{
				ksfCanvas.setLoading(false);
				ksfGraphTools.showFeedback(FEEDBACK_DANGER, "Error", response.error)
			}
			else if (response.done)
			{
				window.location.href = ksfData.baseUrl() + FILE_VIEW_HASH + gateRedirect;
			}
			else
			{
				//The server may have told the client to give up before finishing its polling cycle
				if (response.giveup)
				{
					ksfCanvas.setLoading(false);
					ksfGraphTools.showFeedback(FEEDBACK_DANGER, "Failed", "Something went wrong; the server cannot fulfil the gating request.")
				}
				else
				{
					if (ksfGraphTools.timeoutCounter != 0)
					{
						setTimeout(
							function()
							{
								ksfGraphTools_setGraphUrl(url, newFilename, ksfGraphTools.timeoutCounter-1);
							},
							//set adjusted timeout if the server has told the client to back off
							GRAPH_POLL_INTERVAL + (response.backoff ? response.backoff : 0) );
					}
					else
					{
						ksfCanvas.setLoading(false);
						ksfGraphTools.showFeedback(FEEDBACK_DANGER, "Timeout", "Graph loading failed, try refreshing the page")
					}
				}
			}
		},
		//on error getting gating status
		function(jqxhr, textStatus, error)
		{
			ksfGraphTools.showFeedback(FEEDBACK_DANGER, textStatus, error)
		}
	);
}
ksfGraphTools.setGraphUrl = ksfGraphTools_setGraphUrl;

/**
 * Allows one to reload properly the image of the graph
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfGraphTools_reloadImage()
{
	ksfGraphTools.timeoutCounter--;
	if (ksfGraphTools.timeoutCounter === 0)
	{
		ksfCanvas.setLoading(false);
		ksfGraphTools.showFeedback(FEEDBACK_DANGER, "Timeout", "Graph loading failed, try refreshing the page")
	}
	else
	{
		$("#graph-img").attr("src", $("#graph-img").attr("src"));
	}
}
ksfGraphTools.reloadImage = ksfGraphTools_reloadImage;

/**
 * Calculate the angle to the horizontal of a vector
 * \param tx - [int] x coordinate of the vector
 * \param ty - [int] y coordinate of the vector
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfGraphTools_mesureAngle(tx, ty)
{
	var angle;
	if (tx === 0)
	{
		angle = ty > 0 ? Math.PI/2 : -Math.PI/2;
	}
	else if (ty === 0)
	{
		angle = tx > 0 ? 0 : Math.PI;
	}
	else
	{
		angle = tx > 0 ? Math.atan(ty/tx) : Math.atan(ty/tx)-Math.PI;
	}
	
	return angle
}
ksfGraphTools.mesureAngle = ksfGraphTools_mesureAngle;

/**
 * Popup a feedback on the app panel
 * \param type - [String] type of the alert: FEEDBACK_[INFO|WARNING|DANGER|SUCCESS]
 * \param title - [String] title of the message
 * \param message - [String] message of the alert
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfGraphTools_showFeedback(type, title, message)
{
	$(".alert").remove();
	var alert = "<div class=\"alert "+type+" alert-dismissable\"> " +
	"<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button> "+ 
	"<strong>"+title+"</strong> "+message+
	"</div>";
	$(CONTENT_AREA).prepend(alert);
}
ksfGraphTools.showFeedback = ksfGraphTools_showFeedback;
