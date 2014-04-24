/**
 * \file app/static/js/graphTools.js
 * \brief JavaScript library to manage graph related tools
 * \author mrudelle@keesaco.com of Keesaco
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

/**
 *	List of gating states.
 */
WAIT  = 0;
WORK  = 1;
WORK2 = 2;
DONE  = 3;
MOVE  = 4;

/**
 *	Sensitivity of moving gate points.
 */
SENSITIVITY = 24;

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
	state : WAIT,
	startx : null,
	starty : null,
	endx : null,
	endy : null,

	move_point : null,
	START_POINT : 0,
	END_POINT : 1,

	ELEMENT_ID : "#tool_rectangular_gating",

	onGraphClick : function(event)
	{
		// Calculate relative mouse position.
		var posX = event.pageX - $(GRAPH_ID).offset().left,
			posY = event.pageY - $(GRAPH_ID).offset().top;

		// If waiting for gate, add start point.
		if (this.state === WAIT)
		{
			this.startx = posX;
			this.starty = posY;
			ksfCanvas.toolText("You just started with the rectangle tool " + (posX) + ' , ' + (posY));
			this.state = WORK;
		}
		// If currently gating, add end point.
		else if (this.state === WORK)
		{
			this.endx = posX;
			this.endy = posY;
			ksfCanvas.drawBox(this.startx, this.starty, this.endx - this.startx, this.endy - this.starty, 1);
			ksfCanvas.toolText("You just finished with the rectangle tool [" + "(" + this.startx + "," + this.starty + ")"  + ' , ' + "(" + this.endx + "," + this.endy + ")" + ']');
			ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
			this.state = DONE;
		}
		// If gating is finished, check for moving points.
		else if (this.state === DONE)
		{
			// Move start point.
			if (this.distance(posX, posY, this.startx, this.starty) < SENSITIVITY)
			{
				this.move_point = this.START_POINT;
				this.state = MOVE;
				ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
				ksfCanvas.toolText("Moving gate.");
			}
			// Move end point.
			else if (this.distance(posX, posY, this.endx, this.endy) < SENSITIVITY)
			{
				this.move_point = this.END_POINT;
				this.state = MOVE;
				ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
				ksfCanvas.toolText("Moving gate.");
			}
		}
		// If moving is finished, move gate.
		else if (this.state === MOVE)
		{
			this.state = DONE;
			// If moving start point.
			if (this.move_point === this.START_POINT)
			{
				this.startx = posX;
				this.starty = posY;
			}
			// If moving end point.
			else if (this.move_point === this.END_POINT)
			{
				this.endx = posX;
				this.endy = posY;
			}
			ksfCanvas.drawBox(this.startx, this.starty, this.endx - this.startx, this.endy - this.starty, 1);
			ksfCanvas.setCursor('crosshair');
		}
	},

	onGraphMouseMove : function(event)
	{
		// Calculate relative mouse position.
		var posX = event.pageX - $(GRAPH_ID).offset().left,
			posY = event.pageY - $(GRAPH_ID).offset().top;
		// If gating is underway draw rectangle from start to mouse position.
		if (this.state === WORK)
		{
			ksfCanvas.drawBox(this.startx, this.starty, posX - this.startx, posY - this.starty, 0.5);
		}
		// If gating is done draw rectangle from start to end.
		else if (this.state === DONE)
		{
			ksfCanvas.drawBox(this.startx, this.starty, this.endx - this.startx, this.endy - this.starty, 1);
			// Change cursor when close to points.
			if ((this.distance(posX, posY, this.startx, this.starty) < SENSITIVITY)
				|| (this.distance(posX, posY, this.endx, this.endy) < SENSITIVITY))
			{
				ksfCanvas.setCursor("move");
			}
			else
			{
				ksfCanvas.setCursor("crosshair");
			}
		}
		// If gate is being moved draw rectangle from point to mouse.
		else if (this.state === MOVE)
		{
			// If moving start point.
			if (this.move_point === this.START_POINT)
			{
				ksfCanvas.drawBox(posX, posY, this.endx - posX, this.endy - posY, 0.5);
			}
			// If moving end point.
			else if (this.move_point === this.END_POINT)
			{
				ksfCanvas.drawBox(this.startx, this.starty, posX - this.startx, posY - this.starty, 0.5);
			}
			// Set cursor.
			ksfCanvas.setCursor('move');
		}
	},

	resetTool : function()
	{
		this.state = WAIT;
		this.starty = null;
		this.startx = null;
		this.endy = null;
		this.endx = null;
		ksfCanvas.clear();
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
		ksfCanvas.toolText("The rectangle has been reset.");
	},

	requestGating : function()
	{
		if (this.state !== DONE)
		{
			ksfCanvas.toolText("Gate is not ready to send.");
			return;
		}
		ksfGraphTools.sendGatingRequest('rectangular_gating', [this.startx, this.starty, this.endx, this.endy]);
	},

	distance : function(x1, y1, x2, y2)
	{
		var x_pow = Math.pow(x1 - x2, 2),
			y_pow = Math.pow(y1 - y2, 2);
		return Math.sqrt(x_pow + y_pow);
	}
}

// This tool propose to draw a polygon, the polygon is closed whenever
// ones select a point too close from another or if the new edge cross one of the previous one.
ksfGraphTools.PolygonGating = {

	state : WAIT,
	PointList : [],
	xList : [],
	yList : [],
	ELEMENT_ID : "#tool_polygon_gating",
	START_RADIUS : 10,

	onGraphClick : function(event)
	{
		// Calculate mouse relative position.
		var x, y, d;
		var posX = event.pageX - $(GRAPH_ID).offset().left,
			posY = event.pageY - $(GRAPH_ID).offset().top;

		// If gating, draw gate polygon.
		if ((this.state === WAIT) || (this.state == WORK))
		{
			// Triggered when the path is closed
			if (this.distanceToStart(posX, posY) < this.START_RADIUS)
			{
				this.state = DONE;
				ksfCanvas.drawPolygon(this.xList, this.yList, this.xList[0], this.yList[0], this.START_RADIUS, 1);
				ksfCanvas.toolText("Selection is finished: "+ (this.xList.length) + " points");
				ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
			}
			else
			{
				this.state = WORK;
				this.xList.push(posX);
				this.yList.push(posY);
				ksfCanvas.drawPolygon(this.xList, this.yList, null, null, this.START_RADIUS, 0.5);
				ksfCanvas.toolText("point #"+ (this.xList.lengt) +": ("+posX+","+posY+")");
			}
		}
		// If gating has finished, reset tool.
		else if (this.state === DONE)
		{
			this.resetTool();
		}
	},

	resetTool : function()
	{
		this.state = WAIT;
		this.xList = [];
		this.yList = [];
		ksfCanvas.clear();
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
	},

	onGraphMouseMove : function(event)
	{
		ksfCanvas.setCursor('crosshair');
		// If gating has finished.
		if (this.state === DONE)
		{
			ksfCanvas.drawPolygon(this.xList, this.yList, this.xList[0], this.yList[0], this.START_RADIUS);
			ksfCanvas.toolText("selection is finished: "+ (this.xList.length) + "points");
		}
		// If gating is in progress.
		else
		{
			// Calculate relative mouse position.
			var posX = event.pageX - $(GRAPH_ID).offset().left,
				posY = event.pageY - $(GRAPH_ID).offset().top;
			// Draw
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

	state : WAIT,
	params : null,
	centerx : null, 
	centery : null, 
	r1 : null, 
	pointx : null, 
	pointy : null, 

	ELEMENT_ID : "#tool_oval_gating",

	onGraphClick : function(event)
	{
		// Calculate relative mouse position.
		var posX = event.pageX - $(GRAPH_ID).offset().left,
			posY = event.pageY - $(GRAPH_ID).offset().top;

		// If waiting to gate, add centroid.
		if (this.state === WAIT)
		{
			this.centerx = posX;
			this.centery = posY;
			ksfCanvas.toolText("Select the smaller radius");
			this.state = WORK;
		}
		// If gating stage 1, add radius.
		else if (this.state === WORK)
		{
			this.r1 = Math.sqrt(Math.pow(this.centerx - posX, 2) + Math.pow(this.centery - posY, 2));
			ksfCanvas.toolText("Select the oval\'s last point");
			this.state = WORK2;
		}
		// If gating stage 2, add last point.
		else if (this.state === WORK2)
		{
			this.pointx = posX;
			this.pointy = posY;
			ksfCanvas.drawOval(this.centerx, this.centery, this.r1, this.pointx, this.pointy, 0.5);
			ksfCanvas.toolText("Oval correctly selected");
			ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
			this.state = DONE;
		}
		// If gating has finished, reset tool.
		else if (this.state === DONE)
		{
			this.resetTool();
		}

	},

	onGraphMouseMove : function(event)
	{
		// Calculate relative mouse position.
		var posX = event.pageX - $(GRAPH_ID).offset().left,
			posY = event.pageY - $(GRAPH_ID).offset().top;

		// If gating stage 1, draw circle with mouse position.
		if (this.state === WORK)
		{
			var r = Math.sqrt(Math.pow(this.centerx - posX, 2) + Math.pow(this.centery - posY, 2));
			ksfCanvas.drawOval(this.centerx, this.centery, r, null, null, 0.5);
		}
		// If gating stage 2, draw ellipsoid with mouse position.
		else if (this.state === WORK2)
		{
			ksfCanvas.drawOval(this.centerx, this.centery, this.r1, posX, posY, 0.5);
		}
		// If gating is done, draw final ellipsoid.
		else if (this.state === DONE)
		{
			ksfCanvas.drawOval(this.centerx, this.centery, this.r1, this.pointx, this.pointy, 1);
		}
	},

	resetTool : function()
	{
		this.state = WAIT;
		this.centerx = null; 
		this.centery = null; 
		this.r1 = null; 
		this.pointx = null; 
		this.pointy = null; 
		ksfCanvas.clear();
		ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
		ksfCanvas.toolText("Select oval\'s center");
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
