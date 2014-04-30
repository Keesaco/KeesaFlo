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
 * Defines the id for the file selector.
 */
FILE_SELECTOR_ID = '#sidebar';

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
	var fileSelector = $(FILE_SELECTOR_ID);
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
	$(FILE_SELECTOR_ID).animate({
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
	$(FILE_SELECTOR_ID).animate({
		marginRight: -$(FILE_SELECTOR_ID).outerWidth()
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
	if(parseInt($(FILE_SELECTOR_ID).css('marginRight'), 10) < 0)
	{
		$(FILE_SELECTOR_ID).css( { marginRight: -$(FILE_SELECTOR_ID).outerWidth() } );
	}
}
ksfLayout.fileSelectorResize = ksfLayout_fileSelectorResize;


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


/**
 * Shows the 'Files' button on the nav bar.
 * \author jmccrea@keesaco.com of Keesaco
 * \author swhitehouse@keesaco.com of Keesaco
 */
function ksfLayout_filesButtonShow()
{
	$(".togglefiles").show();
}
ksfLayout.filesButtonShow = ksfLayout_filesButtonShow;


function ksfLayout_filesButtonHide()
{
	ksfLayout.fileSelectorOut();
	$(".togglefiles").hide();
}
ksfLayout.filesButtonHide = ksfLayout_filesButtonHide;


/*
 * Hooks file selector repositioning to the window being resized.
 */
$(window).resize(ksfLayout.fileSelectorResize);


/**
 * Sets up file preview view for new file
 * \author mrudelle@keesaco.com of Keesaco
 */
function ksfLayout_filePreviewStart()
{
	ksfCanvas.addListener();
	$("#togglefiles").click(ksfLayout.fileSelectorToggle);
	$("#btn-change-axes-confirm").click(function () { ksfGraphTools.changeAxes(); } )
}
ksfLayout.filePreviewStart = ksfLayout_filePreviewStart;

/**
 * Enables or disables the upload button on the upload modal
 * \param Bool state - true disables the button, false enables
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfLayout_setUploadButtonDisabled(state)
{
	$('#uploadModal').find('[value="upload"]').prop('disabled', state);
}
ksfLayout.setUploadButtonDisabled = ksfLayout_setUploadButtonDisabled;


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
		style: 		{ classes: 'qtip-dark qtip-shadow qtip-rounded' },
		show:		{ delay: 800 },
		hide:		{ event: 'mouseleave click' },
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
					viewport: $('#appmain')
				},
				style : {
				   classes: 'file-preview-tip qtip-bootstrap qtip-shadow qtip-rounded'
				},
				content: {
					text: function(event, api)
					{
						var prevUrl = ksfData.baseUrl() + "panels/vol/graph_preview/file=" + api.elements.target.children('.file-list-link').first().attr('href').split('/preview/')[1];
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
					  	//TODO: refactor
						return '<div class="loading" style="width: 200px; height:200px">&nbsp</div>';
					}
				},
			};
			$(this).qtip($.extend(true, {}, qTipOptions, eventExt), event);
		} )
}
ksfLayout.initTips = ksfLayout_initTips;
