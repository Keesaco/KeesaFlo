/**
 * \file app/static/js/helptools.js
 * \brief Allows display of on screen assistance for gating.
 * \author swhitehouse@keesaco.com of Keesaco
 */
/**
 * \package app.static.js.helptools
 * \brief Provides methods for controlling on screen assistance for gating.
 */


/**
 * ksfHelpTools constructor used for namespace.
 * \note This constructor declares the namespace.
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools(){}


/*
 * These are function bindings from ksfCanvas, allowing the descriptions and steps to be shown.
 */
ksfHelpTools.stepShow = ksfCanvas.toolText
ksfHelpTools.descriptionShow = ksfCanvas.toolDescription;


/**
 * Shows help for the rectangle gating tool.
 * \param step - the step that needs to be shown
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools_rectangleHelpShow(step)
{
	switch(step)
	{
		case 0:
			ksfHelpTools.descriptionShow(
				"The rectangle tool is used to select rectangular areas of the graph to focus on or remove using reverse gate."
			);
			ksfHelpTools.stepShow(
				"Click to place the first corner."
			);
			break;
		case 1:
			ksfHelpTools.stepShow(
				"Click to place the opposite corner."
			);
			break;
		case 2:
			ksfHelpTools.stepShow(
				"Click to drag highlighted corners. When you're happy, click \"Gate\"."
			);
			break;
		default:
			ksfHelpTools.stepShow(
				""
			);
			break;
	}
}
ksfHelpTools.rectangleHelpShow = ksfHelpTools_rectangleHelpShow;


/**
 * Shows help for the polygon gating tool.
 * \param step - the step that needs to be shown
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools_polygonHelpShow(step)
{
	switch(step)
	{
		case 0:
			ksfHelpTools.descriptionShow(
				"The polygon tool is used to select a polygonal areas of the graph to focus on or remove using reverse gate."
			);
			ksfHelpTools.stepShow(
				"Click to place vertices."
			);
			break;
		case 1:
			ksfHelpTools.stepShow(
				"Click to drag highlighted vertices. When you're happy, click \"Gate\"."
			);
			break;
		default:
			ksfHelpTools.stepShow(
				""
			);
			break;
	}
}
ksfHelpTools.polygonHelpShow = ksfHelpTools_polygonHelpShow;


/**
 * Shows help for the elliptical gating tool.
 * \param step - the step that needs to be shown
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools_ellipseHelpShow(step)
{
	switch(step)
	{
		case 0:
			ksfHelpTools.descriptionShow(
				"The ellipse tool is used to select a elliptical areas of the graph to focus on or remove using reverse gate."
			);
			ksfHelpTools.stepShow(
				"Click to place the centre point."
			);
			break;
		case 1:
			ksfHelpTools.stepShow(
				"Click to determine the size of the first axis."
			);
			break;
		case 2:
			ksfHelpTools.stepShow(
				"Click to determine the size of the second axis, and the orientation."
			);
			break;
		case 3:
			ksfHelpTools.stepShow(
				"Click to drag highlighted points. When you're happy, click \"Gate\"."
			);
			break;
		default:
			ksfHelpTools.stepShow(
				""
			);
			break;
	}
}
ksfHelpTools.ellipseHelpShow = ksfHelpTools_ellipseHelpShow;


/**
 * Shows help for the boolean OR gating tool.
 * \param step - the step that needs to be shown
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools_boolorHelpShow(step)
{
	switch(step)
	{
		case 0:
			ksfHelpTools.descriptionShow(
				"The boolean OR tool is used to focus on the union of the two polygonal regions selected, or remove it using reverse gate."
			);
			ksfHelpTools.stepShow(
				"Click to place vertices for the first gate."
			);
			break;
		case 1:
			ksfHelpTools.stepShow(
				"Click to place vertices for the second gate."
			);
			break;
		case 2:
			ksfHelpTools.stepShow(
				"Click to drag highlighted vertices. When you're happy, click \"Gate\"."
			);
			break;
		default:
			ksfHelpTools.stepShow(
				""
			);
			break;
	}
}
ksfHelpTools.boolorHelpShow = ksfHelpTools_boolorHelpShow;


/**
 * Shows help for the quadrant gating tool.
 * \param step - the step that needs to be shown
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools_quadrantHelpShow(step)
{
	switch(step)
	{
		case 0:
			ksfHelpTools.descriptionShow(
				"The quadrant tool is used to split the graph into four separate plots."
			);
			ksfHelpTools.stepShow(
				"Click to place the origin."
			);
			break;
		case 1:
			ksfHelpTools.stepShow(
				"Click to drag the origin. When you're happy, click \"Gate\"."
			);
			break;
		default:
			ksfHelpTools.stepShow(
				""
			);
			break;
	}
}
ksfHelpTools.quadrantHelpShow = ksfHelpTools_quadrantHelpShow;


/**
 * Shows help for the normal distribution gating tool.
 * \param step - the step that needs to be shown
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools_normdistHelpShow(step)
{
	switch(step)
	{
		case 0:
			ksfHelpTools.descriptionShow(
				"The normal distribution tool fits a bivariate normal distribution to the data and excludes all cells more than one standard deviation away from the mean."
			);
			ksfHelpTools.stepShow(
				"Click \"Gate\" to gate this graph using normal distribution."
			);
			break;
		default:
			ksfHelpTools.stepShow(
				""
			);
			break;
	}
}
ksfHelpTools.normdistHelpShow = ksfHelpTools_normdistHelpShow;


/**
 * Shows help for the K-means gating tool.
 * \param step - the step that needs to be shown
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelpTools_kmeansHelpShow(step)
{
	switch(step)
	{
		case 0:
			ksfHelpTools.descriptionShow(
				"The k-means tool splits the data into three clusters based on the distribution of the data along the x-axis."
			);
			ksfHelpTools.stepShow(
				"Click \"Gate\" to gate this graph using K-means."
			);
			break;
		default:
			ksfHelpTools.stepShow(
				""
			);
			break;
	}
}
ksfHelpTools.kmeansHelpShow = ksfHelpTools_kmeansHelpShow;

