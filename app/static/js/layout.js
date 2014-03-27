/*
 * constructor used for namespace
 * \author mrudelle@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfLayout() {
}

FILE_SIDEBAR_ID = '#sidebar';
TOOLBAR_ID = '#sidebar2';
APP_PANEL_CLASS = '.apppanel'
TOOLBAR_WIDTH = '50px';

ksfLayout.fileSelectorPanel;
ksfLayout.toolbarPanel;
ksfLayout.appPanel;


/*
 * Adds hook to toggle elements (for the toolbar and the filebar)
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
ksfLayout_addToggleHook = function()
{
    var fileSelectorPanel = $(FILE_SIDEBAR_ID);
    var toolbarPanel = $(TOOLBAR_ID);
	var appPanel = $(APP_PANEL_CLASS);
	
    //Handle the filebar behaviour
    $(window).resize( function() {
		if(parseInt(fileSelectorPanel.css('marginRight'), 10) < 0)
		{
			fileSelectorPanel.css( { marginRight: -fileSelectorPanel.outerWidth() } );
		}
	} );
	
    //Handle the toolbar behaviour
    $(window).resize( function() {
		var browserWidth = $(window).width();
		if(browserWidth > 767 && parseInt(toolbarPanel.css('marginLeft'), 10) == 0)
		{
			toolbarPanel.css( { marginLeft: '0' } );
		}
		else if (browserWidth > 767)
		{
			toolbarPanel.css( { marginLeft: '0' } );
		}
		else
		{
			toolbarPanel.css( { marginLeft: ("-" + TOOLBAR_WIDTH) } );
		}
	} );
}
ksfLayout.addToggleHook = ksfLayout_addToggleHook;

ksfLayout_toggleToolBar = function()
{
    var toolbarPanel = $(TOOLBAR_ID);
	var appPanel = $(APP_PANEL_CLASS);
	
	toolbarPanel.animate( {
		marginLeft: parseInt(toolbarPanel.css('marginLeft'), 10) == 0
			? ("-" + TOOLBAR_WIDTH)
			: 0 });
	
    appPanel.animate( {
		marginLeft: parseInt(appPanel.css('marginLeft'), 10) == 0
		? TOOLBAR_WIDTH
		: 0 });
}
ksfLayout.toggleToolBar = ksfLayout_toggleToolBar;

/*
 * Toggle the file selector panel
 * \author hdoughty@keesaco.com of Keesaco
 * \author mrudelle@keesaco.com of Keesaco
 */
ksfLayout_toggleFileSelector = function()
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

/*
 * Oppens the file selector panel
 * \author swhitehouse@keesaco.com of Keesaco
 */
ksfLayout_closeFileSelector = function()
{
	$(FILE_SIDEBAR_ID).fileSelectorPanel.animate( { marginRight: 0 } );
}
ksfLayout.closeFileSelector = ksfLayout_closeFileSelector;

ksfLayout_filePreviewStart = function() {
	ksfCanvas.addListener();
	$("#file-selector-open").click(ksfLayout.toggleFileSelector);
}
ksfLayout.filePreviewStart = ksfLayout_filePreviewStart;