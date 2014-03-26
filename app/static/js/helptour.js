/**
 * \file app/static/js/helptour.js
 * \brief Bootstrap tour based help tour for the application.
 * \author swhitehouse@keesaco.com of Keesaco
 */

/** \package app.static.js.helptour
 * \brief Provides methods for controlling the help tour.
 */


/**
 * ksfHelp constructor used for namespace
 * \author swhitehouse@keesaco.com of Keesaco
 * \return None
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfHelp()
{
}

var ksfHelp_pathURL = ksfData.baseUrl();

// The bootstrap-tour object which handles the tour.
var ksfHelp_mainTour = new Tour
({
	name:		"ksfHelp_mainTour",
	steps:		[
					{
						title:		"Welcome to KeesaFlo!",
						content:	"KeesaFlo is a collaborative flow-cytometry analysis application.",
						backdrop:	true,
						orphan:		true,
						next:		2,
						prev:		-1
					},
					{
						title:		"Welcome to KeesaFlo!",
						content:	"KeesaFlo is a collaborative flow-cytometry analysis application.",
						backdrop:	true,
						orphan:		true,
						next:		3,
						prev:		-1
					},
					{
						element: 	".tour-step.account",
						placement: 	"left",
						title: 		"Account Options",
						content: 	"Click here for settings, to logout, or to go through this tour again.",
						next:		4,
						prev:		0
					},
					{
						element:	".tour-step.account",
						placement:	"bottom",
						title: 		"Account Options",
						content: 	"Click here for settings, to logout, or to go through this tour again.",
						next:		5,
						prev:		1,
						onShow:		function(tour)
									{
										setDropDown(true);
									},
						onPrev:		function()
									{
										setDropDown(false);
									}
					},
					{
						element: 	".tour-step.files",
						placement: 	"left",
						title: 		"Files",
						content: 	"This button shows the file panel, allowing you access to all of your previously uploaded flow cytometry files.",
						next:		6,
						prev:		2
					},
					{
						element:	".tour-step.files",
						placement:	"bottom",
						title: 		"Files",
						content: 	"This button shows the file panel, allowing you access to all of your previously uploaded flow cytometry files.",
						next:		7,
						prev:		3,
						onShow:		function(tour)
									{
										setDropDown(true);
									}
					},
					{
						element: 	".tour-step.upload",
						placement: 	"top",
						title: 		"Upload",
						content: 	"Click this button to upload your new flow cytometry (.fcs) data.",
						next:		8,
						prev:		4,
						onShow:		function()
									{
										setFileBar(true);
									},
						onNext:		function()
									{
										setFileBar(false);
									},
						onPrev:		function()
									{
										setFileBar(false);
									}
					},
					{
						element: 	".tour-step.upload",
						placement: 	"top",
						title: 		"Upload",
						content: 	"Click this button to upload your new flow cytometry (.fcs) data.",
						next:		9,
						prev:		5,
						onShow:		function()
									{
										setDropDown(true);
										setFileBar(true);
									},
						onNext:		function()
									{
										setFileBar(false);
										setDropDown(false);
									},
						onPrev:		function()
									{
										setFileBar(false);
									}
					},
					{
						element:	".tour-step.tools",
						placement:	"right",
						title:		"Tools",
						content:	"Use these tools to gate your flow cytometry files.",
						next:		10,
						prev:		6
					},
					{
						element:	".tour-step.tools",
						placement:	"right",
						title:		"Tools",
						content:	"Use these tools to gate your flow cytometry files.",
						next:		11,
						prev:		7,
						onShow:		function()
									{
										setDropDown(false);
										setToolBar(true);
									},
						onNext:		function()
									{
										setToolBar(false);
									},
						onPrev:		function()
									{
										setToolBar(false);
									}
					},
					{
						title:		"The End",
						content:	"We hope you enjoy using Keesaflo. If you have any questions, check the FAQ in the bottom left corner.",
						orphan:		true,
						next:		-1,
						prev:		8,
						onNext:		function()
									{
										ksfHelp_mainTour.end();
									}
					},
					{
						title:		"The End",
						content:	"We hope you enjoy using Keesaflo. If you have any questions, check the FAQ in the bottom left corner.",
						orphan:		true,
						next:		-1,
						prev: 		9
					}
				]
});

// Shows the tool bar on true, hides on false.
function setToolBar(is_out)
{
	if(is_out)
	{
		$('#sidebar2').animate({
			marginLeft: 0
		});
		$('.apppanel').animate({
			marginLeft: 50
		});
	}
	else{
		$('#sidebar2').animate({
			marginLeft: -50
		});
		$('.apppanel').animate({
			marginLeft: 0
		});
	}
}

// Shows the drop down on true, hides on false.
function setDropDown(is_out)
{
	if(is_out)
	{
		$('#dropdownmenu').collapse('show');
	}
	else{
		$('#dropdownmenu').collapse('hide');
	}
}

// Shows the file bar on true, hides on false.
function setFileBar(is_out)
{
	if(is_out)
	{
		$('#sidebar').animate({
			marginRight: 0
		});
	}
	else{
		$('#sidebar').animate({
			marginRight: -$('#sidebar').outerWidth()
		});
	}
}

// Function to begin the help tour.
function ksfHelp_mainTourBegin(force)
{
	if(force)
	{
		if(ksfHelp_mainTour.ended())
		{
			ksfHelp_mainTour.restart();
		}
	}
	else
	{
		ksfHelp_mainTour.start();
	}
	if(ksfHelp_mainTour.ended() == false)
	{
		if($(window).width() <= 767)
		{
			ksfHelp_mainTour.setCurrentStep(1);
			ksfHelp_mainTour.goTo(1);
		}
	}
}
ksfHelp.mainTourBegin = ksfHelp_mainTourBegin;

//Function to end the help tour.
function ksfHelp_mainTourEnd()
{
	ksfHelp_mainTour.end();
}
ksfHelp.mainTourEnd = ksfHelp_mainTourEnd;

// Updated the help tour when the window is resized.
$(function(){
	$(window).resize(function() {
		if(ksfHelp_mainTour.ended() == false)
		{
			var $browserWidth = $(window).width();
			currentStep = ksfHelp_mainTour.getCurrentStep();
			if($browserWidth <= 767)
			{
				if((currentStep % 2) == 0)
				{
					currentStep += 1;
					
				}
			}
			else{
				if((currentStep % 2) == 1)
				{
					currentStep -= 1;
				}
			}
			ksfHelp_mainTour.setCurrentStep(currentStep);
			ksfHelp_mainTour.goTo(currentStep);
		}
	});
});

// Initialize the tour
ksfHelp_mainTour.init();

// Runs the help tour.
ksfHelp.mainTourBegin(false);

