/**
 * \file app/static/js/tools.js
 * \brief JavaScript library for setting up the tool module of the app page
 * \author mrudelle@keesaco.com of Keesaco
 */
/**
 * \package app.static.js.tools
 * \brief Provides methods for selecting a tool
 */

TOOLS_LIST = [ksfGraphTools.RectangularGating, ksfGraphTools.PolygonGating, ksfGraphTools.OvalGating, ksfGraphTools.NormalGating, ksfGraphTools.QuadrantGating, ksfGraphTools.KmeansGating, ksfGraphTools.OrGating];

ksfTools.CurrentTool = null;

/**
 * ksfTools constructor used for namespace
 * \author mrudelle@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfTools()
{
}

/**
 * change the selected tool as well as active classes according to the element triggering this function
 * \param event - given by javascript when a tool is selected
 * \author mrudelle@keesaco.com of Keesaco
 */
ksfTools.switchTool = function(event)
{
	// TODO: Might be replaced by a reversed hash of TOOLS_LIST
	var i = TOOLS_LIST.length - 1;
	for (; i >= 0 && TOOLS_LIST[i].ELEMENT_ID !== ("#" + this.id) ; i--) {}
	if (ksfTools.CurrentTool)
	{
		ksfTools.CurrentTool.resetTool();
	}
	ksfTools.CurrentTool = TOOLS_LIST[i];
	ksfTools.CurrentTool.resetTool();
	$(ksfTools.CurrentTool.ELEMENT_ID).addClass('active')
		.siblings('.active').removeClass('active');
}

/**
 * Set the listener on each tool of the toolList
 * \author mrudelle@keesaco.com of Keesaco
 */
ksfTools.addToolsListener = function() 
{
	for (var i = TOOLS_LIST.length - 1; i >= 0; i--)
	{
		$(TOOLS_LIST[i].ELEMENT_ID).click(ksfTools.switchTool);
	}
}