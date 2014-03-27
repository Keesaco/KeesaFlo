/*
 * \file app/static/js/appstart.js
 * \brief Sets the hook on the page and pagelet when they are fetched
 * \author mrudelle@keesaco.com of Keesaco
 * \author hdoughty@keesaco.com of Keesaco
 */

 $("#help-tour-begin").click(function() { helpTourBegin(true); });
 

qTipOptions =
{
style: 		{ classes: 'qtip-bootstrap qtip-shadow qtip-rounded' },
position: 	{ container: $('div.tooltips') }
};
$(document).ready(function()
{
	$("#help-force-start").click(helpTourBegin(true));
	appstart.addToggleHook();
	
	tipSelector = $('[title!=""]').not('.notip');
	[	{ name: '.tip-right',	ext: { position: {my: 'center left', at: 'center right' } } },
		{ name: '.tip-left', 	ext: { position: {my: 'center right', at: 'center left' } } },
		{ name: '.tip-top', 	ext: { position: {my: 'bottom center', at: 'top center' } } },
		{ name: '.tip-bottom', 	ext: { position: {my: 'top center', at: 'bottom center' } } } ]
		.forEach( function(t) {
			tipSelector.filter(t.name).qtip($.extend(true, {}, qTipOptions, t.ext ) );
		} );

});


/*
* constructor used for namespace
* \author mrudelle@keesaco.com of Keesaco
* \note This constructor currently (intentionally) does not have any effect
*/
function appstart() {
}

FILE_SIDE_BAR = '#sidebar';
TOOL_BAR_ID = '#sidebar2';
APP_PANEL_ID = '.apppanel'
TOOLBAR_WIDTH = '50px';

appstart.fileSelectorPanel;
appstart.toolbarPanel;
appstart.appPanel;

/*
* Contains all the code to run after a new graph is fetched
* \author mrudelle@keesaco.com of Keesaco
*/
appstart_filePreviewStart = function() {
	//var filename = $('#filename").text();
	ksfCanvas.addListener();
	$("#file-selector-open").click(appstart.toggleFileSelector);
	//ksfData_copyPageletInto(ksfData.baseUrl() + 'panels/main/fetch_info' + encodeURIComponent('=' + filename), CONTENT_AREA, appstart.file
}
appstart.filePreviewStart = appstart_filePreviewStart;

/*
* Adds hook to toggle elements (for the toolbar and the filebar)
* \author hdoughty@keesaco.com of Keesaco
* \author mrudelle@keesaco.com of Keesaco
*/
appstart_addToggleHook = function() 
{
    appstart.fileSelectorPanel = $(FILE_SIDE_BAR);
    appstart.toolbarPanel = $(TOOL_BAR_ID);
	appstart.appPanel = $(APP_PANEL_ID);

    $('.togglefiles').click(appstart.toggleFileSelector);
    $('.toggletools').click(appstart.toogleToolBar);

    //Handle the filebar behaviour
    $(window).resize(function() {
        if(parseInt(appstart.fileSelectorPanel.css('marginRight'), 10) < 0) {
            appstart.fileSelectorPanel.css({
                marginRight: -appstart.fileSelectorPanel.outerWidth()
            });
        }
    });

    //Handle the toolbar behaviour
    $(window).resize(function() {
        var browserWidth = $(window).width();
        if(browserWidth > 767 && parseInt(appstart.toolbarPanel.css('marginLeft'), 10) == 0) {
            appstart.toolbarPanel.css({
                marginLeft: '0'
            });
        }
        else if(browserWidth > 767) {
            appstart.toolbarPanel.css({
                marginLeft: '0'
            });
        }
        else {
            appstart.toolbarPanel.css({
                marginLeft: ("-" + TOOLBAR_WIDTH)
            });
        }
    });
}
appstart.addToggleHook = appstart_addToggleHook;

appstart_toogleToolBar = function()
{
	appstart.toolbarPanel.animate({
        marginLeft: parseInt(appstart.toolbarPanel.css('marginLeft'), 10) == 0 ?
            ("-" + TOOLBAR_WIDTH) : 0
    });
    appstart.appPanel.animate({
        marginLeft: parseInt(appstart.appPanel.css('marginLeft'), 10) == 0 ?
            TOOLBAR_WIDTH : 0
    });
}
appstart.toogleToolBar = appstart_toogleToolBar;

/*
* Toggle the file selector panel
* \author hdoughty@keesaco.com of Keesaco
* \author mrudelle@keesaco.com of Keesaco
*/
appstart_toggleFileSelector = function()
{
    appstart.fileSelectorPanel.animate({
        marginRight: parseInt(appstart.fileSelectorPanel.css('marginRight'), 10) == 0 ?
        -appstart.fileSelectorPanel.outerWidth() : 0
    });
    var browserWidth = $(window).width();
    if(browserWidth <= 767 && parseInt(appstart.fileSelectorPanel.css('marginRight'), 10) < 0) {
        $('#dropdownmenu').toggleClass('collapse');
        $('#dropdownmenu').toggleClass('in');
    }
}
appstart.toggleFileSelector = appstart_toggleFileSelector;

/*
* Oppens the file selector panel
* \author swhitehouse@keesaco.com of Keesaco
*/
appstart_closeFileSelector = function()
{
    appstart.fileSelectorPanel.animate({
        marginRight: 0
    });
}
appstart.closeFileSelector = appstart_closeFileSelector;
