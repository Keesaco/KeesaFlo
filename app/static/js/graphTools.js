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

FEEDBACK_SUCCESS = "alert-success";
FEEDBACK_INFO = "alert-info";
FEEDBACK_WARING = "alert-warning";
FEEDBACK_DANGER = "alert-danger";
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
        ksfGraphTools.sendGatingRequest('gating/rectangular/' + this.startx + "," + this.starty + "," + this.endx + "," + this.endy, "rect_gating");
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
        ksfGraphTools.sendGatingRequest(URL, "poly_gating");
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
        var tx = this.centerx-this.pointx,
            ty = this.centery-this.pointy;
        var angle = ksfGraphTools.mesureAngle(tx, ty);
        var p1x=this.centerx+Math.cos(angle-Math.PI/2)*this.r1,
        p1y=this.centery+Math.sin(angle-Math.PI/2)*this.r1;
        ksfGraphTools.sendGatingRequest("gating/oval/" + this.centerx + "," + this.centery + "," + p1x + "," + p1y + "," + this.pointx + "," + this.pointy, "oval_gating");
    }
}

/*!************************************************************************
** \fn ksfGraphTools.sendGatingRequest()
** \brief Perform a gating request and update the view correspondingly
** \param gatingURL - [String] url of the gating command
** \param suffix - [String] suffix to be added at the end of the new file
** \author mrudelle@keesaco.com of Keesaco
** \note This might be moved to views.js in the future
***************************************************************************/
ksfGraphTools.sendGatingRequest = function(gatingURL, suffix) {
    if (suffix === undefined) {
        suffix = "gating";
    }
    // allows to fetch the name correctly. In the future (final release) this should be replace by a json file fetched from the server containing all the file's data
    $("#filesize").remove();
    var filename = $("#filename").text() + "-" + suffix;
    ksfCanvas.toolText("loading...");

    ksfReq.fetch(   gatingURL + "," + filename, 
                    function(response)
                        {
                            console.log("answer get");
                            ksfGraphTools.showFeedback(
                                response.status === "success" ? FEEDBACK_SUCCESS :
                                response.status === "fail" ? FEEDBACK_DANGER: FEEDBACK_INFO,
                                response.status, response.message);
                            ksfCanvas.toolText("");
                            $("#graph-img").attr("src", response.imgUrl);
                            $("#filename").text(filename);
                        },
                    function()
                        {
                             ksfGraphTools.showFeedback(FEEDBACK_DANGER, "fail", "the server failed to respond to the gating request");
                        } );
}

/*!************************************************************************
** \fn ksfGraphTools.mesureAngle()
** \brief Calculate the angle of a vector
** \param tx - [int] x coordinate of the vector
** \param ty - [int] y coordinate of the vector
** \author mrudelle@keesaco.com of Keesaco
***************************************************************************/
ksfGraphTools.mesureAngle = function(tx, ty) {
    var angle;
    if (tx === 0) {
        angle = ty > 0 ? Math.PI/2 : -Math.PI/2;
    } else if (ty === 0) {
        angle = tx > 0 ? 0 : Math.PI;
    } else {
        angle = tx > 0 ? Math.atan(ty/tx) : Math.atan(ty/tx)-Math.PI;
    }
    return angle
}

/*!************************************************************************
** \fn ksfGraphTools.showFeedback()
** \brief Popup a feedback on the app panel
** \param type - [String] type of the alert: FEEDBACK_[INFO|WARNING|DANGER|SUCCESS]
** \param title - [String] title of the message
** \param message - [String] message of the alert
** \author mrudelle@keesaco.com of Keesaco
***************************************************************************/
ksfGraphTools.showFeedback = function(type, title, message) {
    $(".alert").remove();
    var alert = "<div class=\"alert "+type+" alert-dismissable\"> " +
    "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button> "+ 
    "<strong>"+title+"</strong> "+message+
    "</div>";
    $(CONTENT_AREA).prepend(alert);
}