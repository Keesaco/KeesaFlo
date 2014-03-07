/*!************************************************************************
 ** \file app/static/js/graphTools.js
 ** \brief JavaScript library to manage graph related tools
 ** \author mrudelle@keesaco.com of Keesaco
 ***************************************************************************
 ** \package app.static.js.graphTools
 ** \brief Provides methods for triggering tool event
 **************************************************************************/

/*!************************************************************************
** \fn ksfGraphTools()
** \brief ksfTools constructor used for namespace
** \author mrudelle@keesaco.com of Keesaco
** \note This constructor currently (intentionally) does not have any effect
***************************************************************************/
function ksfGraphTools() {
}

// Allows one to fetch the graph element of the page
GRAPH_ID = "#flow-canvas";
GRAPH_ID_RAW = "flow-canvas";
TOOL_POPOVER_TITLE = "tool-popover-title";

var context;
var canvas;

/*
    Each of the folowing elements represent a graph related tool
    they contains - an ELEMENT_ID that allows one to access the tool's button
                  - a function onGraphClick, trigered by a click on the graph when this tool is selected
                  - a function resetTool, called when the tool is unselected
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

    onGraphClick : function(event) {
        var posX = event.pageX - $(GRAPH_ID).offset().left,
        posY = event.pageY - $(GRAPH_ID).offset().top;

        if ((this.startx === null) || (this.starty === null)) {
            this.startx = posX;
            this.starty = posY;
            document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "You just started with the rectangle tool " + (posX) + ' , ' + (posY);
        } else if ((this.endx === null) || (this.endy === null)){
            this.endx = posX;
            this.endy = posY;
            context.strokeRect(this.startx, this.starty, this.endx-this.startx, this.endy-this.starty);
            document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "You just finished with the rectangle tool [" + "(" + this.startx + "," + this.starty + ")"  + ' , ' + "(" + this.endx + "," + this.endy + ")" + ']';
        } else {
            this.resetTool();
            context.clearRect(0, 0, canvas.width, canvas.height);
            document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "The rectangle has been reset.";
        }
    },

    onGraphMouseMove : function(event) {
        var posX = event.pageX - $(GRAPH_ID).offset().left,
        posY = event.pageY - $(GRAPH_ID).offset().top;
        if (((this.endx === null) || (this.endy === null)) && ((this.startx !== null) || (this.starty !== null))) {
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.strokeRect(this.startx, this.starty, posX-this.startx, posY-this.starty);
        }
    },

    resetTool : function() {
        this.starty = null;
        this.startx = null;
        this.endy = null;
        this.endx = null;
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

}

// This tool propose to draw a polygon, the polygon is closed whenever
// ones select a point too close from another or if the new edge cross one of the previous one.
ksfGraphTools.PolygonGating = {

    PointList : [],
    SelectionDone : false,
    ELEMENT_ID : "#tool_polygon_gating",
    START_RADIUS : 5,

    onGraphClick : function(event) {
        if (this.SelectionDone) {
            return;
        }
        
        var posX, posY, x, y, d;

        posX = event.pageX - $(GRAPH_ID).offset().left;
        posY = event.pageY - $(GRAPH_ID).offset().top;

        // Triggered when the path is closed
        if (this.distanceToStart(posX, posY) < this.START_RADIUS){
            this.drawPolygon(null, null);
            this.SelectionDone = true;
            document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "selection is finished: "+ (this.PointList.length/2) + "points";
        } else {
            this.PointList.push(posX);
            this.PointList.push(posY);
            this.drawPolygon(null, null);
            document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "point #"+ (this.PointList.length/2) +": ("+posX+","+posY+")";
        }
    },

    resetTool : function() {
        this.PointList = [];
        this.SelectionDone = false;
        context.clearRect(0, 0, canvas.width, canvas.height);
    },

    onGraphMouseMove : function(event) {
        $(GRAPH_ID).css( 'cursor', 'crosshair' );
        if (this.SelectionDone) {
            this.drawPolygon(this.PointList[0], this.PointList[1]);
            document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "selection is finished: "+ (this.PointList.length/2) + "points";
        } else {
            var posX = event.pageX - $(GRAPH_ID).offset().left,
            posY = event.pageY - $(GRAPH_ID).offset().top;
            this.drawPolygon(posX, posY);
            if (this.distanceToStart(posX, posY) < this.START_RADIUS){
                $(GRAPH_ID).css( 'cursor', 'pointer' );
            }
        }
    },

    drawPolygon : function(lastx, lasty) {
        if (this.PointList.length < 2 || ((lastx === null || lasty === null) && this.PointList.length < 4)) {
            return;
        }

        context.clearRect(0, 0, canvas.width, canvas.height);
        context.beginPath();
        context.fillStyle = "rgba(255, 0, 0, 0.5)";
        context.arc(this.PointList[0], this.PointList[1], this.START_RADIUS, 0, Math.PI*2);
        context.fill();
        context.moveTo(this.PointList[0], this.PointList[1]);
        for (var i = 2; i < this.PointList.length ; i+=2) {
            context.lineTo(this.PointList[i], this.PointList[i+1]);
        };
        if (lastx !== null || lasty !== null){
            context.lineTo(lastx, lasty);
        }
        context.stroke();
        context.closePath();
    },
    
    distanceToStart : function(posx, posy){
        var x, y;
        if (this.PointList.length >= 2) {
            x = this.PointList[0]-posx;
            y = this.PointList[1]-posy;
            return Math.sqrt(Math.pow(x,2)+Math.pow(y,2));
        }
        return Math.MAX;
    }
}

//This tool allows one to create an oval shaped selection
//It's behaviour remains to be specified
ksfGraphTools.OvalGating = {
    params : null,

    ELEMENT_ID : "#tool_oval_gating",

    onGraphClick : function(event) {
        var posX = event.pageX - $(GRAPH_ID).offset().left,
        posY = event.pageY - $(GRAPH_ID).offset().top;
        document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "The oval tool remains to be implemented";
    },
    
    onGraphMouseMove : function(event) {
        
    },

    resetTool : function() {
        this.starty = null;
        this.startx = null;
        this.endy = null;
        this.endx = null;
        //TODO: might be moved to a graphReset function
        context.clearRect(0, 0, canvas.width, canvas.height);
    }
}

/*!************************************************************************
** \fn ksfGraphTools.addListener()
** \brief set a click listener to the graph
** \author mrudelle@keesaco.com of Keesaco
** \note The listener triggers the proper tool's onGraphClick() function
***************************************************************************/
ksfGraphTools.addListener = function() 
{
    $(GRAPH_ID).css('cursor', 'crosshair');
    $(GRAPH_ID).click(function(event) {
        if (ksfTools.CurrentTool && ksfTools.CurrentTool.onGraphClick) {
            if (canvas.width===0 || canvas.height===0){
                ksfGraphTools.fixCanvasSize();
            }
            ksfTools.CurrentTool.onGraphClick(event);
        } else {
            document.getElementById(TOOL_POPOVER_TITLE).innerHTML = "You must choose a tool.";
        }
    });
    $(GRAPH_ID).mousemove(function(event) {
        if (ksfTools.CurrentTool && ksfTools.CurrentTool.onGraphClick) {
            ksfTools.CurrentTool.onGraphMouseMove(event);
        }
    });
    var tool_popover = document.getElementById(TOOL_POPOVER_TITLE);
    if (tool_popover !== null) {
        tool_popover.innerHTML = "You must choose a tool.";
    }
    
    if (ksfTools.CurrentTool !== null){
        ksfTools.CurrentTool.resetTool();
    }
    
    canvas = document.getElementById(GRAPH_ID_RAW);
    if (canvas !== null){
        canvas.width = 0;
        canvas.height = 0;
        context = canvas.getContext('2d');
    }
    
}

ksfGraphTools.fixCanvasSize = function() {
    canvas.width = document.getElementById("flow-graph-container").clientWidth;
    canvas.height = document.getElementById("flow-graph-container").clientHeight;
}
