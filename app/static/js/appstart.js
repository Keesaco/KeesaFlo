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
	ksfHelp.mainTourInit();
	$('.togglefiles').click(ksfLayout.fileSelectorToggle);
				  
	//upload button
	//prevents clicking 'upload' twice
	$('#frm-new-file-upload').on('submit', function() { ksfLayout.setUploadButtonDisabled(true); return true; } );
	//re-enable the button when the modal closes
	$('#uploadModal').on('hidden.bs.modal', function () { ksfLayout.setUploadButtonDisabled(false); });
});