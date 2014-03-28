/**
 * \file app/static/js/appstart.js
 * \brief Hooks listeners and runs other code which needs to execute when the application first loads
 * \author jmccrea@keesaco.com of Keesaco
 */
 
$(document).ready(function()
{
	ksfViews.loadFromLocation(true);
	ksfHelp.mainTourInit();
	$("#ksf-help-begin").click(ksfHelp.mainTourBegin);
	$('.togglefiles').click(ksfLayout.fileSelectorToggle);
});