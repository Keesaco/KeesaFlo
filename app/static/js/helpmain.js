/**
 * \file app/static/js/helpmain.js
 * \brief Bootstrap tour based help tour for the application.
 * \author swhitehouse@keesaco.com of Keesaco
 */
/**
 * \package app.static.js.helpmain
 * \brief Provides methods for controlling the help tour.
 */


/**
 * ksfHelp constructor used for namespace.
 * \note This constructor declares the namespace.
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelp(){}


/**
 * Initialises the help tour.
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelp_mainTourInit()
{
	ksfHelp_mainTour.init();
	ksfHelp_mainTour.start();
}
ksfHelp.mainTourInit = ksfHelp_mainTourInit;


/**
 * Adapts the help tour to the current screen size.
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelp_mainTourResize()
{
	if(ksfHelp_mainTour.ended() == false)
	{
		var browserWidth = $(window).width();
		var currentStep = ksfHelp_mainTour.getCurrentStep();
		if(browserWidth <= LAYOUT_WIDTH_THRESHOLD)
		{
			if((currentStep % 2) == 0)
			{
				currentStep += 1;	
			}
		}
		else
		{
			if((currentStep % 2) == 1)
			{
				currentStep -= 1;
			}
		}
		ksfHelp_mainTour.setCurrentStep(currentStep);
		ksfHelp_mainTour.goTo(currentStep);
	}
}
ksfHelp.mainTourResize = ksfHelp_mainTourResize;


/**
 * Begins the help tour.
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelp_mainTourBegin()
{
	if(ksfHelp_mainTour.ended())
	{
		ksfHelp_mainTour.restart();
	}
	ksfHelp_mainTourResize();
}
ksfHelp.mainTourBegin = ksfHelp_mainTourBegin;


/**
 * Checks whether the help tour is still in focus, and if not ends it.
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelp_mainTourRefocus(event)
{
	if(!ksfHelp_mainTour.ended())
	{
		if($(event.target).parents('.tour-ksfHelp_mainTour').length == 0)
		{
			ksfHelp.mainTourEnd();
		}
	}
}
ksfHelp.mainTourRefocus = ksfHelp_mainTourRefocus;


/**
 * Ends the help tour.
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfHelp_mainTourEnd()
{
	ksfHelp_mainTour.end();
}
ksfHelp.mainTourEnd = ksfHelp_mainTourEnd;


/**
 * The variable that holds the help tour.
 * \author swhitehouse@keesaco.com of Keesaco
 */
ksfHelp_mainTour = new Tour
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
			onShow:		ksfLayout.dropDownIn,
			onPrev:		ksfLayout.dropDownOut
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
			onShow:		ksfLayout.dropDownIn
		},
		{
			element: 	".tour-step.upload",
			placement: 	"top",
			title: 		"Upload",
			content: 	"Click this button to upload your new flow cytometry (.fcs) data.",
			next:		8,
			prev:		4,
			onShow:		ksfLayout.fileSelectorIn,
			onNext:		ksfLayout.fileSelectorOut,
			onPrev:		ksfLayout.fileSelectorOut
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
							ksfLayout.fileSelectorIn();
							ksfLayout.dropDownIn();
						},
			onNext:		function()
						{
							ksfLayout.fileSelectorOut();
							ksfLayout.dropDownOut();
						},
			onPrev:		ksfLayout.fileSelectorOut
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
			onShow:		ksfLayout.dropDownOut
		},
		{
			title:		"The End",
			content:	"We hope you enjoy using Keesaflo. If you have any questions, check the FAQ in the bottom left corner.",
			orphan:		true,
			next:		-1,
			prev:		8,
			onNext:		ksfHelp.mainTourEnd
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

