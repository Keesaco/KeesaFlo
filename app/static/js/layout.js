/**
 * \file app/static/js/layout.js
 * \brief Contains code for interacting with UI elements suce as slide-out toolbars
 * \author jmccrea@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 */

/**
 * constructor used for namespace
 * \author mrudelle@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfLayout() {
}

FILE_SIDEBAR_ID = '#sidebar';
APP_PANEL_CLASS = '.apppanel'
TOOLBAR_WIDTH = '50px';

/**
 * Adds hook to toggle elements (for the toolbar and the filebar)
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_addToggleHook()
{
    var fileSelectorPanel = $(FILE_SIDEBAR_ID);
	var appPanel = $(APP_PANEL_CLASS);
	
    //Handle the filebar behaviour
    $(window).resize( function() {
		if(parseInt(fileSelectorPanel.css('marginRight'), 10) < 0)
		{
			fileSelectorPanel.css( { marginRight: -fileSelectorPanel.outerWidth() } );
		}
	} );
}
ksfLayout.addToggleHook = ksfLayout_addToggleHook;

/**
 * Toggle the file selector panel
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_toggleFileSelector()
{
	var fileSelectorPanel = $(FILE_SIDEBAR_ID);
	
    fileSelectorPanel.animate( {
		marginRight: parseInt(fileSelectorPanel.css('marginRight'), 10) == 0
			? -fileSelectorPanel.outerWidth()
			: 0 } );
	
    var browserWidth = $(window).width();
    if(browserWidth <= 767 && parseInt(fileSelectorPanel.css('marginRight'), 10) < 0)
	{
        $('#dropdownmenu').toggleClass('collapse');
        $('#dropdownmenu').toggleClass('in');
    }
}
ksfLayout.toggleFileSelector = ksfLayout_toggleFileSelector;

/**
 * Oppens the file selector panel
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfLayout_closeFileSelector()
{
	$(FILE_SIDEBAR_ID).fileSelectorPanel.animate( { marginRight: 0 } );
}
ksfLayout.closeFileSelector = ksfLayout_closeFileSelector;

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