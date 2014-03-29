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
TOOLBAR_ID = '#sidebar2';
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

/**
 * Opens or closes the tool selector depending on its current state
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfLayout_toggleToolBar()
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
	/**
	 * Options to be applied to all tooltips
	 */
	var qTipOptions =
	{
		style: 		{ classes: 'qtip-bootstrap qtip-shadow qtip-rounded' },
		show:		{ delay: 800 },
		overwrite: 	false,
	};
	var tipSelector = $('[title!=""]').not('.notip');
	
	/* */
	[	{ name: '.tip-right',	ext: { position: { my: 'center left', at: 'center right' } } },
		{ name: '.tip-left', 	ext: { position: { my: 'center right', at: 'center left' } } },
		{ name: '.tip-top', 	ext: { position: { my: 'bottom center', at: 'top center' } } },
		{ name: '.tip-bottom', 	ext: { position: { my: 'top center', at: 'bottom center' } } } ]
		.forEach( function(t) {
			$(tipSelector).on('mouseover', t.name,
			function(event)
			{
				var eventExt =
				{
					show: {
						  event: event.type,
						  ready: true
					}
				};
				$(this).qtip($.extend(true, {}, eventExt, t.ext, qTipOptions), event);
			} )
			.each(function(i) {
				// removed to prevent error, TODO: reinstate and fix
				  
				//$.attr(this, 'oldtitle', $.attr(this, 'title'));
				//this.removeAttribute('title');
			  });
		} );
		
	$(document).on('mouseover', '.file-list-item',
		function(event)
		{
			var eventExt =
			{
				show: {
					event: event.type,
					ready: true
				},
				position: {
					my: 'right center',
					at: 'left center',
					viewport: $('#appmain'),
					target: 'event'
				},
				content: {
					text: function(event, api)
					{
						var prevUrl = ksfData.baseUrl() + "panels/vol/graph_preview/file=" + api.elements.target.attr('href').split('/preview/')[1];
						$.ajax( {
							   url: prevUrl
						} )
						.then(
							function(content) {
								api.set('content.text', content);
							},
							function(xhr, status, error) {
								api.set('content.text', status + ': ' + error);
							});
					  
						return 'Loading...'; 
					}
				},
			};
			$(this).qtip($.extend(true, {}, eventExt, qTipOptions), event);
		} )
	
	
}
ksfLayout.initTips = ksfLayout_initTips;