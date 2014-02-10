/*!************************************************************************
 ** \file app/static/js/views.js
 ** \brief JavaScript library for setting up views within the app page
 ** \author jmccrea@keesaco.com of Keesaco
 ***************************************************************************
 ** \package app.static.js.views
 ** \brief Provides methods for modifying data from the data layer for use by the front-end UI
 **************************************************************************/

$(document).ready(
function()
{
	ksfViews.setupView();
	ksfViews.loadView();
});

/*!************************************************************************
** \fn ksfViews()
** \brief ksfViews constructor used for namespace
** \author jmccrea@keesaco.com of Keesaco
** \note This constructor currently (intentionally) does not have any effect
***************************************************************************/
function ksfViews()
{
}

CONTENT_AREA = '#appmain';
FILE_SELECTOR = '#filelist';

/*!************************************************************************
** \fn ksfViews.loadView()
** \brief sets up a view based on the current URL
** \author jmccrea@keesaco.com of Keesaco
***************************************************************************/
ksfViews.setupView = function()
{
	var urlVals = ksfData.urlValues();
	switch ( urlVals[0] )
	{
		case 'preview':
		case '':
			ksfViews.setupDefault();
			break;
			
		case 'faq':
		case 'about':
			ksfViews.setupSimple();
			break;
			
		default:
			ksfViews.setupDefault();
	}
}

ksfViews.loadView = function()
{
	var urlVals = ksfData.urlValues();
	switch ( urlVals[0] )
	{
		case 'preview':
			ksfViews.loadPreview( urlVals.length > 0 ? urlVals[1] : '' );
			break;
			
		case 'faq':
			ksfViews.loadFAQ();
			break;
			
		case 'about':
			ksfView.loadAbout();
			break;
	}
}

ksfViews.refreshAll = function()
{
	ksfProc.loadView();
}

ksfViews.setupDefault = function()
{
	//ksfViews.showFilebar(true);
	//ksfViews.showToolSelector(true);
}

ksfViews.setupSimple = function()
{
	//ksfViews.showFilebar(false);
	//ksfViews.showToolSelector(false);
}

ksfViews.showFilebar = function(show)
{
	if ( show )
	{
		$(".togglefiles").show();
		$("#filelist").css( { marginRight: '0px' } );
	}
	else
	{
		$(".togglefiles").hide();
		var fl = $("#filelist");
		fl.css( { marginRight: fl.outerWidth() } );
	}
}

ksfViews.showToolSelector = function(show)
{
	if ( show )
	{
		//$("#toolselectorhead").show();
		//$("#toolselector").css( { marginLeft: '0px' } );
	}
	else
	{
		//$("#toolselectorhead").hide();
		//var ts = $("#toolselector");
		//ts.css( { marginLeft: ts.outerWidth() } );
	}
}

ksfViews.loadPreview = function(filename)
{
	ksfData.copyPageletInto( ksfData.baseUrl() + '/file=' + filename, CONTENT_AREA );
	ksfData.copyPageletInto( ksfData.baseUrl() + '/file_list/', FILE_SELECTOR );
}

ksfViews.loadFAQ = function()
{
	ksfData.copyPageletInto( ksfData.baseUrl() + '/faw'
}

ksfViews.loadAbout = function()
{
	
}
