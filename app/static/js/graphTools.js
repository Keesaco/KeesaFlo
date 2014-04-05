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

ksfGraphTools.timeoutCounter = 10;

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
		if (((this.endx === null) || (this.endy === null)) && ((this.startx !== null) || (this.starty !== null))) {
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
		ksfGraphTools.sendGatingRequest('gating/rectangular/' + this.startx + "," + this.starty + "," + this.endx + "," + this.endy);
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
		var URL = "gating/polygon/" + this.xList.concat(this.yList).join(",");
		ksfGraphTools.sendGatingRequest(URL);
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
				ksfCanvas.drawOval(this.centerx, this.centery, r, null, null);
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
		ksfGraphTools.sendGatingRequest("gating/oval/" + this.centerx + "," + this.centery + "," + p1x + "," + p1y + "," + this.pointx + "," + this.pointy);
	}
}

/**
 * Perform a gating request and update the view correspondingly
 * \param gatingURL - [String] url of the gating command
 * \author mrudelle@keesaco.com of Keesaco
 * \note This might be moved to views.js in the future
 */
function ksfGraphTools_sendGatingRequest(gatingURL)
{
	// allows to fetch the name correctly. In the future (final release) this should be replace by a json file fetched from the server containing all the file's data
	
	$("#filesize").remove();
	var filename = $("#filename").text().trim();
	
	ksfTools.CurrentTool.resetTool();
	ksfCanvas.toolText("Loading graph...");

	ksfReq.fetch(   gatingURL + "," + filename, 
					function(response)
					{
						ksfGraphTools.showFeedback(
							response.status === "success" ? FEEDBACK_SUCCESS :
							response.status === "fail" ? FEEDBACK_DANGER: FEEDBACK_INFO,
							response.status, response.message);
						ksfCanvas.toolText("");
						$("#filename").text(filename);
						ksfGraphTools.setGraphUrl(response.imgUrl);
					},
					function()
					{
						ksfGraphTools.showFeedback(FEEDBACK_DANGER, "fail", "The server failed to respond to the gating request");
					} );
}
ksfGraphTools.sendGatingRequest = ksfGraphTools_sendGatingRequest;

/**
 * Change properly the graph image
 * \param url - [String] url of the new graph
 * \author mrudelle@keesaco.com of Keesaco
 * \note If the link throw an error it will enter a loop to reload the image
 */
function ksfGraphTools_setGraphUrl(url)
{
	// we let 10 sec for the graph to appear
	ksfGraphTools.timeoutCounter = 10;
	$("#graph-img").off('error');
	$("#graph-img").on('error', function()
		{
			ksfCanvas.setLoading(true);
			setTimeout(ksfGraphTools.reloadImage, 1000);
		} );
	$("#graph-img").on('load', function()
		{
			ksfCanvas.setLoading(false);
		});
	$("#graph-img").attr("src", url);
}
ksfGraphTools.setGraphUrl = ksfGraphTools_setGraphUrl;

/**
 * Allows one to reload properly the image of the graph
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfGraphTools_reloadImage()
{
	ksfGraphTools.timeoutCounter--;
	if (ksfGraphTools.timeoutCounter === 0) {
		ksfCanvas.setLoading(false);
		ksfGraphTools.showFeedback(FEEDBACK_DANGER, "Timeout", "Graph loading failed, try refreshing the page")
	} else {
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
