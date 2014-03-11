function ksfCanvas(){
}

// Allows one to fetch the elements of the page
GRAPH_ID = "#flow-canvas";
TOOL_POPOVER_TITLE = "#tool-popover-title";
REQUEST_GATING_BTN = "#request-gating-btn";
RESET_TOOL_BTN = "#reset-tool-btn";

var context;
var canvas;
var tool_popover;

// Print the selection box on the screen
ksfCanvas.drawBox = function(ax, ay, bx, by, alpha) {
	this.clear();
    context.save();
    context.fillStyle = "rgba(255, 0, 0, "+alpha/2+")";
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
	this.clear();
	
    if (pointList.length < 2) {
        return;
    };

    context.beginPath();
    context.fillStyle = "rgba(255, 0, 0, 0.5)";
    context.arc(pointList[0], pointList[1], startRadius, 0, Math.PI*2);
    context.fill();
    context.closePath();

    if (((lastx === null || lasty === null) && pointList.length < 4)) {
        return;
    }

	context.beginPath();
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
	this.clear();
	
    var r2, angle, tx, ty;
	var alpha = 1;
	if (p2x !== null && p2y !== null) {
		tx = cx-p2x;
		ty = cy-p2y;
    	r2 = Math.sqrt(Math.pow(cx-p2x,2)+Math.pow(cy-p2y,2));
		if (tx === 0) {
        	angle = Math.PI/2;
		} else if (ty === 0) {
			angle = 0;
		} else {
			angle = Math.atan(ty/tx);
		}
	} else {
		r2 = r1;
		angle = 0;
	}
	
	context.beginPath();
    context.fillStyle = "rgba(255, 0, 0, "+(alpha/2)+")";
    context.arc(cx, cy, 5, 0, Math.PI*2);
	context.closePath();
    context.arc(p2x, p2y, 5, 0, Math.PI*2);
	context.closePath();
	if (p2x !== null && p2y !== null){
		var p1x=cx+Math.cos(angle-Math.PI/2)*r1,
		p1y=cy+Math.sin(angle-Math.PI/2)*r1;
		context.arc(p1x, p1y, 5, 0, Math.PI*2);
		context.closePath();
	}
    context.fill();
	
	
    context.save();
	
    context.beginPath();
	context.translate(cx,cy);
	context.rotate(angle);
	context.scale(r2/r1,1);
	
    context.arc(0, 0, r1, 0, Math.PI*2);
    context.restore();
    context.stroke();
}

ksfCanvas.toolText = function(msg) {
    if (tool_popover !== null) {
        tool_popover.text(msg);
    }
}


ksfCanvas.clear = function() {
    if (context !== null && canvas !== undefined) {
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
	
	$(RESET_TOOL_BTN).click(function(){
		ksfTools.CurrentTool.resetTool();
	});
	$(REQUEST_GATING_BTN).click(function(){
		ksfTools.CurrentTool.requestGating();
	})
}

ksfCanvas.enableBtn = function(btn, enable){
    if (enable) {
        $(btn).removeAttr("disabled");
    } else {
        $(btn).attr('disabled','disabled');
    }
}