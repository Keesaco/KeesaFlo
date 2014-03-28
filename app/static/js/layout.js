/**
 * \file app/static/js/layout.js
 * \brief Contains code for interacting with panels and other UI elements.
 * \author jmccrea@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 * \author swhitehouse@keesaco.com of Keesaco
 */
/**
 * \package app.static.js.layout
 * \brief Provides methods for interacting with UI elements.
 */

 
 /**
 * Defines the width at which the layout of the web page changes.
 */
LAYOUT_WIDTH_THRESHOLD = 767;

/**
 * Defines the id for the file sidebar.
 */
FILE_SIDEBAR_ID = '#sidebar';

/**
 * Defines the id for the drop down menu (small screens only).
 */
DROP_DOWN_ID = '#dropdownmenu';

/**
 * Defines the id for the app panels (used as margins).
 */
APP_PANEL_CLASS = '.apppanel';


/**
 * Constructor for the ksfLayout namespace.
 * \author mrudelle@keesaco.com of Keesaco
 * \note This constructor does not have any effect and will never be used.
 */
function ksfLayout(){}


/**
 * Toggles whether the file selector panel is in view.
 * \author swhitehouse@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 * \note If the screen is small enough to have the drop down menu, the menu closes.
 */
function ksfLayout_fileSelectorToggle()
{
	var fileSelector = $(FILE_SIDEBAR_ID);
	fileSelector.animate( {
		marginRight: parseInt(fileSelector.css('marginRight'), 10) == 0
			? -fileSelector.outerWidth()
			: 0 } );

	if($(window).width() <= LAYOUT_WIDTH_THRESHOLD)
	{
		ksfLayout.dropDownOut();
	}
}
ksfLayout.fileSelectorToggle = ksfLayout_fileSelectorToggle;


/**
 * Sets the position of the file selector to be in view.
 * \author swhitehouse@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_fileSelectorIn()
{
	$(FILE_SIDEBAR_ID).animate({
		marginRight: 0
	});
}
ksfLayout.fileSelectorIn = ksfLayout_fileSelectorIn;


/**
 * Sets the position of the file selector to be out of view.
 * \author swhitehouse@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_fileSelectorOut()
{
	$(FILE_SIDEBAR_ID).animate({
		marginRight: -$(FILE_SIDEBAR_ID).outerWidth()
	});
}
ksfLayout.fileSelectorOut = ksfLayout_fileSelectorOut;


/**
 * Repositions the file selector based on its size.
 * \author swhitehouse@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_fileSelectorResize()
{
	if(parseInt($(FILE_SIDEBAR_ID).css('marginRight'), 10) < 0)
	{
		$(FILE_SIDEBAR_ID).css( { marginRight: -$(FILE_SIDEBAR_ID).outerWidth() } );
	}
}
ksfLayout.fileSelectorResize = ksfLayout_fileSelectorResize;


/**
 * Toggles whether the drop down panel is in view.
 * \author swhitehouse@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 */
function ksfLayout_dropDownToggle()
{
	
}
ksfLayout.dropDownToggle = ksfLayout_dropDownToggle;


/**
 * Sets the position of the dropdown to be in view.
 * \author swhitehouse@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_dropDownIn()
{
	$('#dropdownmenu').collapse('show');
}
ksfLayout.dropDownIn = ksfLayout_dropDownIn;


/**
 * Sets the position of the dropdown to be out of view.
 * \author swhitehouse@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_dropDownOut()
{
	$('#dropdownmenu').collapse('hide');
}
ksfLayout.dropDownOut = ksfLayout_dropDownOut;


/*
 * Hooks file selector repositioning to the window being resized.
 */
$(window).resize(ksfLayout.fileSelectorResize);


/**
 * Sets up file preview view for new file
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfLayout_filePreviewStart()
{
	ksfCanvas.addListener();
	$("#file-selector-open").click(ksfLayout.toggleFileSelector);
}
ksfLayout.filePreviewStart = ksfLayout_filePreviewStart;


/**
 * Sets up tooltip classes
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfLayout_initTips()
{
	var qTipOptions =
	{
		style: 		{ classes: 'qtip-bootstrap qtip-shadow qtip-rounded' },
		position: 	{ container: $('div.tooltips') }
	};
	
	var tipSelector = $('[title!=""]').not('.notip');
	
	[	{ name: '.tip-right',	ext: { position: {my: 'center left', at: 'center right' } } },
		{ name: '.tip-left', 	ext: { position: {my: 'center right', at: 'center left' } } },
		{ name: '.tip-top', 	ext: { position: {my: 'bottom center', at: 'top center' } } },
		{ name: '.tip-bottom', 	ext: { position: {my: 'top center', at: 'bottom center' } } } ]
		.forEach( function(t) {
			 tipSelector.filter(t.name).qtip($.extend(true, {}, qTipOptions, t.ext ) );
		} );
}

