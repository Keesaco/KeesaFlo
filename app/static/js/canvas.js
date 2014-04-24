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

/**
 * Draw a selection box on the canvas
 * \param ax - x coordinate of the first point
 * \param ay - y coordinate of the first point
 * \param bx - x coordinate of the second point
 * \param by - y coordinate of the second point
 * \param alpha - circle transparency
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvasdrawBox(ax, ay, bx, by, alpha)
{
	this.clear();
	context.save();
	context.fillStyle = "rgba(255, 0, 0, " + alpha / 2 + ")";
	context.beginPath();
	context.arc(ax, ay, 5, 0, Math.PI*2);
	context.arc(ax+bx, ay+by, 5, 0, Math.PI*2);
	context.fill();
	context.closePath();
	context.restore();
	context.strokeStyle = "rgba(0, 0, 0, 1)";
	context.strokeRect(ax, ay, bx, by);
	context.restore();
}

ksfCanvas.drawBox = ksfCanvasdrawBox;


/**
 * Draw a polygon on the canvas
 * \param xList - x coordinates of the points
 * \param yList - y coordinates of the points
 * \param lastx - x coordinates of the last points (null if no last point)
 * \param lasty - y coordinates of the last points (null if no last point)
 * \param startRadius - radius of the starting point (red area clickable to close the gate)
 * \param alpha - circle transparency
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_drawPolygon(xList, yList, lastx, lasty, startRadius, alpha)
{
	this.clear();

	if (xList.length < 1)
	{
		return;
	}

	context.beginPath();
	context.fillStyle = "rgba(255, 0, 0, " + alpha / 2 + ")";
	context.arc(xList[0], yList[0], startRadius, 0, Math.PI*2);
	context.fill();
	context.closePath();

	if (((lastx === null || lasty === null) && xList.length < 2))
	{
		return;
	}

	context.beginPath();
	context.moveTo(xList[0], yList[0]);
	for (var i = 1; i < xList.length ; i++)
	{
		context.lineTo(xList[i], yList[i]);
	}

	if (lastx !== null || lasty !== null)
	{
		context.lineTo(lastx, lasty);
	}
	context.stroke();
	context.closePath();
}

ksfCanvas.drawPolygon = ksfCanvas_drawPolygon;

/**
 * Draws an oval on the canvas
 * \param cx - x coordinates of the center points
 * \param cy - y coordinates of the center points
 * \param r1 - first radius of the oval
 * \param p2x - x coordinates of the last point (it belongs to the oval)
 * \param p2y - y coordinates of the last point (it belongs to the oval)
 * \param alpha - circle transparency
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_drawOval(cx, cy, r1, p2x, p2y, alpha)
{
	this.clear();
	var r2, angle, tx, ty;
	if (p2x !== null && p2y !== null)
	{
		tx=cx-p2x;
		ty=cy-p2y;
		r2 = Math.sqrt(Math.pow(tx,2)+Math.pow(ty,2));
		angle = ksfGraphTools.mesureAngle(tx, ty);
	}
	else
	{
		r2 = r1;
		angle = 0;
	}
	
	context.beginPath();
	context.fillStyle = "rgba(255, 0, 0, " + alpha / 2 + ")";
	context.arc(cx, cy, 5, 0, Math.PI*2);
	context.closePath();
	if (p2x !== null && p2y !== null)
	{
		context.arc(p2x, p2y, 5, 0, Math.PI*2);
		context.closePath();
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

ksfCanvas.drawOval = ksfCanvas_drawOval;

/**
 * Set the text shown over the graph
 * \param msg - [string] text to be shown
 * \note This area is used to provide the user with a short feedback on his actions
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_toolText(msg)
{
	if (tool_popover !== null)
	{
		tool_popover.text(msg);
	}
}

ksfCanvas.toolText = ksfCanvas_toolText;

/**
 * Clear the canvas (erase its content to make it transparent)
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_clear()
{
	if (context !== null && canvas !== undefined)
	{
		context.clearRect(0, 0, canvas.width, canvas.height);
	}
}

ksfCanvas.clear = ksfCanvas_clear;

/**
 * Set the cursor of the graph
 * \param cursor - [string] cursor name as defined by css (see http://www.w3schools.com/cssref/pr_class_cursor.asp)
 * \note This area is used to provide the user with a short feedback on his actions
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_setCursor(cursor)
{
	$(GRAPH_ID).css( 'cursor', cursor );
}
ksfCanvas.setCursor = ksfCanvas_setCursor;

/**
 * set a click listener to the graph
 * \author mrudelle@keesaco.com of Keesaco
 * \note The listener triggers the proper tool's onGraphClick() function
 */
function ksfCanvas_addListener(argument)
{
	$(GRAPH_ID).css('cursor', 'crosshair');
	$(GRAPH_ID).click(
		function(event)
		{
			if (ksfTools.CurrentTool && ksfTools.CurrentTool.onGraphClick)
			{
				ksfTools.CurrentTool.onGraphClick(event);
			}
			else
			{
				ksfCanvas.toolText("You must choose a tool.");
			}
		} );
	$(GRAPH_ID).mousemove(
		function(event)
		{
			if (ksfTools.CurrentTool && ksfTools.CurrentTool.onGraphClick)
			{
				ksfTools.CurrentTool.onGraphMouseMove(event);
			}
		});

	tool_popover = $(TOOL_POPOVER_TITLE);

	canvas = $(GRAPH_ID)[0];
	if (canvas !== null && canvas !== undefined)
	{
		context = canvas.getContext('2d');
	}
	
	$(RESET_TOOL_BTN).click(
		function()
		{
			ksfTools.CurrentTool.resetTool();
		});
	
	$(REQUEST_GATING_BTN).click(
		function()
		{
			ksfTools.CurrentTool.requestGating();
		} )

	$("#graph-img").off('error');
	$("#graph-img").on('error',
		function()
		{
			ksfCanvas.setLoading(true);
			setTimeout(ksfGraphTools.reloadImage, 1000);
		} );
}
ksfCanvas.addListener = ksfCanvas_addListener;

/**
 * Set the enbabled status of a button
 * \param btn - [string] jquerry name (#id , .class ... etc) that points to the button
 * \param enable - [boolean] define if we want to enable or not the button
 * \note depending on the string this can applies to multiple buttons
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_enableBtn(btn, enable)
{
	if (enable)
	{
		$(btn).removeAttr("disabled");
	}
	else
	{
		$(btn).attr('disabled','disabled');
	}

	if (btn === REQUEST_GATING_BTN && enable)
	{
		ksfCanvas.blinkButton(btn);
	}
}
ksfCanvas.enableBtn = ksfCanvas_enableBtn;

/**
 * Replace the image of the graph by a spinner or the opposit
 * \param enable - [boolean] define if we replace the image by a spinner or not
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_setLoading(enable)
{
	if (enable)
	{
		$(GRAPH_ID).addClass("loading");
		$("#graph-img").css("display", "none");
	}
	else
	{
		$(GRAPH_ID).removeClass("loading");
		$("#graph-img").css("display", "");
	}
}
ksfCanvas.setLoading = ksfCanvas_setLoading;

/**
 * Makes an element blink
 * \param btn - element to blink (#id, .class, etc)
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfCanvas_blinkButton(btn)
{
	var resetBackColor = $(btn).css('background-color');
	var resetColor = $(btn).css('color');
	$(btn).animate(
		{
			"background-color": "#FF8500",
			"color": "#fff"
		}, 200, function()
		{
			$(btn).animate(
			{
			  "background-color": resetBackColor,
			  "color": resetColor
			}, 800);
		} );
}
ksfCanvas.blinkButton = ksfCanvas_blinkButton;
