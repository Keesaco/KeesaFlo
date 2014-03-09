function ksfCanvas(){
}

// Allows one to fetch the elements of the page
GRAPH_ID = "#flow-canvas";
TOOL_POPOVER_TITLE = "#tool-popover-title";

var context;
var canvas;
var tool_popover;

// Print the selection box on the screen
ksfCanvas.drawBox = function(ax, ay, bx, by, alpha) {
    this.clear();
    context.save();
    context.fillStyle = "rgba(255, 0, 0, "+alpha+")";
    context.beginPath();
    context.arc(ax, ay, 5, 0, Math.PI*2);
    context.arc(ax+bx, ay+by, 5, 0, Math.PI*2);
    context.fill();
    context.closePath();
    context.restore();
    context.strokeStyle = "rgba(0, 0, 0, "+alpha+")";
    context.strokeRect(ax, ay, bx, by);
    context.restore();
}

//print the polygon on the canvas
ksfCanvas.drawPolygon = function(pointList, lastx, lasty, startRadius) {
    if (pointList.length < 2 || ((lastx === null || lasty === null) && pointList.length < 4)) {
        return;
    }

    this.clear();
    context.beginPath();
    context.fillStyle = "rgba(255, 0, 0, 0.5)";
    context.arc(pointList[0], pointList[1], startRadius, 0, Math.PI*2);
    context.fill();
    context.moveTo(pointList[0], pointList[1]);
    for (var i = 2; i < pointList.length ; i+=2) {
       context.lineTo(pointList[i], pointList[i+1]);
    };
    if (lastx !== null || lasty !== null){
       context.lineTo(lastx, lasty);
    }
    context.stroke();
    context.closePath();
}

ksfCanvas.drawOval = function(cx, cy, r1, p2x, p2y) {
    
}

ksfCanvas.toolText = function(msg) {
    if (tool_popover !== null) {
        tool_popover.text(msg);
    }
}


ksfCanvas.clear = function() {
    if (context !== null) {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }
}

ksfCanvas.setCursor = function(cursor) {
	$(GRAPH_ID).css( 'cursor', cursor );
}

/*!************************************************************************
** \fn ksfCanvas.addListener()
** \brief set a click listener to the graph
** \author mrudelle@keesaco.com of Keesaco
** \note The listener triggers the proper tool's onGraphClick() function
***************************************************************************/
ksfCanvas.addListener = function(argument) {
	$(GRAPH_ID).css('cursor', 'crosshair');
    $(GRAPH_ID).click(function(event) {
        if (ksfTools.CurrentTool && ksfTools.CurrentTool.onGraphClick) {
            ksfTools.CurrentTool.onGraphClick(event);
        } else {
            ksfCanvas.toolText("You must choose a tool.");
        }
    });
    $(GRAPH_ID).mousemove(function(event) {
        if (ksfTools.CurrentTool && ksfTools.CurrentTool.onGraphClick) {
            ksfTools.CurrentTool.onGraphMouseMove(event);
        }
    });

    tool_popover = $(TOOL_POPOVER_TITLE);

    canvas = $(GRAPH_ID)[0];
    if (canvas !== null && canvas !== undefined){
        context = canvas.getContext('2d');
    }  
}