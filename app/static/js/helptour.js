var tour = new Tour
({
	storage: false,
	debug: true
});

tour.addSteps
([
	{
		title:		"Welcome to KeesaFlo!",
		content:	"KeesaFlo is a collaborative flow-cytometry analysis application.",
		backdrop:	true,
		orphan:		true,
		next:		1,
		prev:		-1,
	},
	{
		element: 	".tour-step.account",
		placement: 	"left",
		title: 		"Account Options",
		content: 	"Click here for settings, to logout, or to go through this tour again.",
		next:		3,
		prev:		0
	},
	{
		element:	".tour-step.account",
		placement:	"bottom",
		title: 		"Account Options",
		content: 	"Click here for settings, to logout, or to go through this tour again.",
		next:		4,
		prev:		0,
		onShow:		function()
					{
						$('#dropdownmenu').collapse('show');
					},
		onPrev:		function()
					{
						$('#dropdownmenu').collapse('hide');
					}
	},
	{
		element: 	".tour-step.files",
		placement: 	"left",
		title: 		"Files",
		content: 	"This button shows the file panel, allowing you access to all of your previously uploaded flow cytometry files.",
		next:		5,
		prev:		1
	},
	{
		element:	".tour-step.files",
		placement:	"bottom",
		title: 		"Files",
		content: 	"This button shows the file panel, allowing you access to all of your previously uploaded flow cytometry files.",
		next:		6,
		prev:		2
	},
	{
		element: 	".tour-step.upload",
		placement: 	"top",
		title: 		"Upload",
		content: 	"Click this button to upload your new flow cytometry (.fcs) data.",
		next:		7,
		prev:		3,
		onShow:		function()
					{
						$('#sidebar').animate({
							marginRight: 0
						});
					},
		onHide:		function()
					{
						$('#sidebar').animate({
							marginRight: -$('#sidebar').outerWidth()
						});
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
						$('#dropdownmenu').collapse('show');
						$('#sidebar').animate({
							marginRight: 0
						});
					},
		onNext:		function()
					{
						$('#sidebar').animate({
							marginRight: -$('#sidebar').outerWidth()
						});
						$('#dropdownmenu').collapse('hide');
					},
		onPrev:		function()
					{
						$('#sidebar').animate({
							marginRight: -$('#sidebar').outerWidth()
						});
					}
	},
	{
		element:	".tour-step.tools",
		placement:	"right",
		title:		"Tools",
		content:	"Use these tools to gate your flow cytometry files.",
		next:		9,
		prev:		5
	},
	{
		element:	".tour-step.tools",
		placement:	"right",
		title:		"Tools",
		content:	"Use these tools to gate your flow cytometry files.",
		next:		9,
		prev:		6,
		onShow:		function()
					{
						$('#sidebar2').animate({
							marginLeft: 0
						});
						$('.apppanel').animate({
							marginLeft: $('#sidebar2').outerWidth()
						});
					},
		onHide:		function()
					{
						$('#sidebar2').animate({
							marginLeft: -$('#sidebar2').outerWidth()
						});
						$('.apppanel').animate({
							marginLeft: 0
						});
					}
	},
	{
		title:		"The End",
		content:	"We hope you enjoy using Keesaflo. If you have any questions, check the FAQ in the bottom left corner.",
		orphan:		true,
		next:		-1,
		prev:		7
	}
]);

// Initialize the tour
tour.init();

// Start the tour
tour.start();

function help_force_start()
{
	if (tour.ended()){
		tour.restart();
	}
	else
	{
		tour.start(true);
	}
}

