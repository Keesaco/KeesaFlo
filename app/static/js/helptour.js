// The bootstrap-tour object which handles the tour.
var keesafloTour = new Tour
({
	name:		"keesaflo-tour",
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
									},
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
						prev:		8
					},
					{
						title:		"The End",
						content:	"We hope you enjoy using Keesaflo. If you have any questions, check the FAQ in the bottom left corner.",
						orphan:		true,
						next:		-1,
						prev: 		9
					}
				],
	debug:		true
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
			marginLeft: $('#sidebar2').outerWidth()
		});
	}
	else{
		$('#sidebar2').animate({
			marginLeft: -$('#sidebar2').outerWidth()
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
function helpTourBegin(force)
{
	if(force)
	{
		keesafloTour.restart();
	}
	else
	{
		keesafloTour.start();
	}
	if($(window).width() <= 767)
	{
		keesafloTour.setCurrentStep(1);
		keesafloTour.goTo(1);
	}
}

// Updated the help tour when the window is resized.
$(function(){
	$(window).resize(function() {
		var $browserWidth = $(window).width();
		currentStep = keesafloTour.getCurrentStep();
		if($browserWidth <= 767)
		{
			if((currentStep % 2) == 0)
			{
				currentStep += 1;
				keesafloTour.setCurrentStep(currentStep);
				keesafloTour.goTo(currentStep);
			}
		}
		else{
			if((currentStep % 2) == 1)
			{
				currentStep -= 1;
				keesafloTour.setCurrentStep(currentStep);
				keesafloTour.goTo(currentStep);
			}
		}
	});
});

// Initialize the tour
keesafloTour.init();

// Runs the help tour.
helpTourBegin(false);

