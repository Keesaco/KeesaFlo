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
            ksfCanvas.toolText("You just started with the rectangle tool " + (posX) + ' , ' + (posY));
        } else if ((this.endx === null) || (this.endy === null)){
            this.endx = posX;
            this.endy = posY;
            ksfCanvas.drawBox(this.startx, this.starty, this.endx-this.startx, this.endy-this.starty, 1);
            ksfCanvas.toolText("You just finished with the rectangle tool [" + "(" + this.startx + "," + this.starty + ")"  + ' , ' + "(" + this.endx + "," + this.endy + ")" + ']');
            ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
        } else {
            this.resetTool();
            ksfCanvas.clear();
            ksfCanvas.toolText("The rectangle has been reset.");
        }
    },

    onGraphMouseMove : function(event) {
        var posX = event.pageX - $(GRAPH_ID).offset().left,
        posY = event.pageY - $(GRAPH_ID).offset().top;
        if (((this.endx === null) || (this.endy === null)) && ((this.startx !== null) || (this.starty !== null))) {
            ksfCanvas.drawBox(this.startx, this.starty, posX-this.startx, posY-this.starty, 0.5);
        }
    },

    resetTool : function() {
        this.starty = null;
        this.startx = null;
        this.endy = null;
        this.endx = null;
        ksfCanvas.clear();
        ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
    },
    
    requestGating : function() {
        ksfGraphTools.sendGatingRequest('gating/rectangular/' + this.startx + "," + this.starty + "," + this.endx + "," + this.endy);
    }
}

// This tool propose to draw a polygon, the polygon is closed whenever
// ones select a point too close from another or if the new edge cross one of the previous one.
ksfGraphTools.PolygonGating = {

    PointList : [],
    SelectionDone : false,
    ELEMENT_ID : "#tool_polygon_gating",
    START_RADIUS : 10,

    onGraphClick : function(event) {
        if (this.SelectionDone) {
            return;
        }
        
        var posX, posY, x, y, d;

        posX = event.pageX - $(GRAPH_ID).offset().left;
        posY = event.pageY - $(GRAPH_ID).offset().top;

        // Triggered when the path is closed
        if (this.distanceToStart(posX, posY) < this.START_RADIUS){
            ksfCanvas.drawPolygon(this.PointList, this.PointList[0], this.PointList[1], this.START_RADIUS);
            this.SelectionDone = true;
            ksfCanvas.toolText("selection is finished: "+ (this.PointList.length/2) + "points");
            ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
        } else {
            this.PointList.push(posX);
            this.PointList.push(posY);
            ksfCanvas.drawPolygon(this.PointList, null, null, this.START_RADIUS);
            ksfCanvas.toolText("point #"+ (this.PointList.length/2) +": ("+posX+","+posY+")");
        }
    },

    resetTool : function() {
        this.PointList = [];
        this.SelectionDone = false;
        ksfCanvas.clear();
        ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
    },

    onGraphMouseMove : function(event) {
        ksfCanvas.setCursor('crosshair');
        if (this.SelectionDone) {
            ksfCanvas.drawPolygon(this.PointList, this.PointList[0], this.PointList[1], this.START_RADIUS);
            ksfCanvas.toolText("selection is finished: "+ (this.PointList.length/2) + "points");
        } else {
            var posX = event.pageX - $(GRAPH_ID).offset().left,
            posY = event.pageY - $(GRAPH_ID).offset().top;
            ksfCanvas.drawPolygon(this.PointList, posX, posY, this.START_RADIUS);
            if (this.distanceToStart(posX, posY) < this.START_RADIUS){
                ksfCanvas.setCursor('pointer');
            }
        }
    },

    //return the distance to the starting point
    distanceToStart : function(posx, posy){
        var x, y;
        if (this.PointList.length >= 2) {
            x = this.PointList[0]-posx;
            y = this.PointList[1]-posy;
            return Math.sqrt(Math.pow(x,2)+Math.pow(y,2));
        }
        return Math.MAX;
    },
    
    requestGating : function() {
        var URL = "gating/polygon/" + this.PointList.join(",");
        ksfGraphTools.sendGatingRequest(URL);
    }
}

//This tool allows one to create an oval shaped selection
//It's behaviour remains to be specified
ksfGraphTools.OvalGating = {
    params : null,
    
    centerx : null, 
    centery : null, 
    r1 : null, 
    pointx : null, 
    pointy : null, 

    ELEMENT_ID : "#tool_oval_gating",

    onGraphClick : function(event) {
        var posX = event.pageX - $(GRAPH_ID).offset().left,
        posY = event.pageY - $(GRAPH_ID).offset().top;
        
        if (this.centerx === null || this.centery === null) {
            this.centerx = posX;
            this.centery = posY;
            ksfCanvas.toolText("select the smaller radius");
        } else if (this.r1 === null) {
            this.r1 = Math.sqrt(Math.pow(this.centerx-posX,2)+Math.pow(this.centery-posY,2));
            ksfCanvas.toolText("select the oval\'s last point")
        } else if (this.pointx === null || this.pointy === null) {
            this.pointx = posX;
            this.pointy = posY;
            ksfCanvas.drawOval(this.centerx, this.centery, this.r1, this.pointx, this.pointy);
            ksfCanvas.toolText("oval corectly selected");
            ksfCanvas.enableBtn(REQUEST_GATING_BTN, true);
        } else {
            this.resetTool();
            ksfCanvas.toolText("select oval\'s center");
        }
        
    },
    
    onGraphMouseMove : function(event) {
        var posX = event.pageX - $(GRAPH_ID).offset().left,
        posY = event.pageY - $(GRAPH_ID).offset().top;

        

        if (this.centerx !== null || this.centery !== null) {
            if (this.r1 === null) {
                var r = Math.sqrt(Math.pow(this.centerx-posX,2)+Math.pow(this.centery-posY,2));
                ksfCanvas.drawOval(this.centerx, this.centery, r, null, null);
            } else if (this.pointx === null || this.pointy === null) {
                ksfCanvas.drawOval(this.centerx, this.centery, this.r1, posX, posY);
            } 
        }
    },

    resetTool : function() {
        this.centerx = null; 
        this.centery = null; 
        this.r1 = null; 
        this.pointx = null; 
        this.pointy = null; 
        ksfCanvas.clear();
        ksfCanvas.enableBtn(REQUEST_GATING_BTN, false);
    },
    
    requestGating : function() {
        ksfGraphTools.sendGatingRequest("gating/oval/" + this.centerx + "," + this.centery + "," + this.r1 + "," + this.pointx + "," + this.pointy);
    }
}


//Might need to be moved to ksfViews
ksfGraphTools.sendGatingRequest = function(gatingURL){
    ksfCanvas.toolText("loading...");
    ksfReq.fetch(gatingURL, function(response){
        ksfCanvas.toolText("Server answered:" + response);
    });
}