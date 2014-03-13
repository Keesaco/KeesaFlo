var tour = new Tour
({
});

tour.addSteps
([
	{
		title:		"Welcome to Keesaflo!",
		content:	"Keesaflo is a collaborative flow-cytometry analysis application. This tour can be started at any time by clicking help in the 'Account Options' menu.",
		backdrop:	true,
		orphan:		true
	},
	{
		element: 	".tour-step.tour-step-one",
		placement: 	"top",
		title: 		"Upload",
		content: 	"Click this button to upload your flow cytometry (.fcs) data."
	},
	{
		element: 	".tour-step.tour-step-two",
		placement: 	"left",
		title: 		"Look at your files",
		content: 	"Click this button will slide out the file panel, allowing you access to all of your previously uploaded flow cytometry files."
	},
	{
		element: 	".tour-step.tour-step-three",
		placement: 	"top",
		title: 		"FAQ",
		content:	"If you have a question, check here to see if it has already been answered."
	},
	{
		element:	".tour-step.tour-step-four",
		placement:	"bottom",
		title: 		"Home",
		content: 	"Click here to get back to the main page."
	},
	{
		element: 	".tour-step.tour-step-five",
		placement: 	"bottom",
		title: 		"Account Options",
		content: 	"Click here for settings, to logout, or to go through this tour again."
	},
	{
		element: 	".tour-step.tour-step-six",
		placement: 	"right",
		title: 		"What the..?",
		content: 	"No one actually knows what this does, just try and ignore it."
	},
	{
		title:		"The End",
		content:	"We hope you enjoy using Keesaflo. Please don't try to gate more than once...",
		orphan:		true
	}
]);

// Initialize the tour
tour.init();

// Start the tour
tour.start();

function force_start()
{
	if (tour.ended()){
		tour.restart();
	}
	else
	{
		tour.start(true);
	}
}

