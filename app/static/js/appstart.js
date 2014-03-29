/**
 * \file app/static/js/appstart.js
 * \brief Hooks listeners and runs other code which needs to execute when the application first loads
 * \author jmccrea@keesaco.com of Keesaco
 */
 
$(document).ready(function()
{
	ksfViews.loadFromLocation(true);
				  
	ksfLayout.initTips();
				  
	$("#ksf-help-begin").click(function() { ksfHelp.mainTourBegin(true); } );
	ksfLayout.addToggleHook();
	ksfHelp.mainTourInit();
	$('.togglefiles').click(ksfLayout.fileSelectorToggle);
});