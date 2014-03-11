/**
 * \file app/static/js/views.js
 * \brief JavaScript library for setting up views within the app page
 * \author jmccrea@keesaco.com of Keesaco
 */

/**
 * \package app.static.js.views
 * \brief Provides methods for modifying data from the data layer for use by the front-end UI
 */



$(document).ready(
function()
{
	ksfViews.loadFromLocation(true)
});


/// \todo This has limited browser compatibility, if this is an issue support for onhashchange could be checked and an alternative timer arrangement provided for older browsers.
window.onhashchange = function ()
{
	ksfViews.loadFromLocation();
}



/**
 * ksfViews constructor used for namespace
 * \author jmccrea@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfViews()
{
}

CONTENT_AREA = '#appmain';
FILE_SELECTOR = '#filelist';
TOOL_SELECTOR = '#toolselector';

ksfViews.currentView = null;

/**
 * sets up a view based on the current URL
 * \tparam String[] urlVals - values taken from the RHS of the hashbang in the URL if found
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_setupViews(urlVals)
{
	switch ( urlVals[0] )
	{
		case 'faq':
		case 'about':
			if (ksfViews.currentView != 'simple')
			{
				ksfViews.currentView = 'simple';
				ksfViews.setupSimple();
			}
			break;
			
		case 'preview':
		case '':
		default:
			if (ksfViews.currentView != 'default')
			{
				ksfViews.currentView = 'default';
				ksfViews.setupDefault();
			}
	}
}
ksfViews.setupView = ksfViews_setupViews;


ksfViews.loadFromLocation = function(force)
{
	var urlVals = ksfData.urlValues();
	if ( urlVals !== null )
	{
		ksfViews.setupView(urlVals);
		ksfViews.loadView(urlVals);
	}
	else if (force)
	{
		ksfViews.setupView(['']);
		ksfViews.loadView(['']);
	}
}

ksfViews.loadView = function(urlVals)
{
	switch ( urlVals[0] )
	{
		case 'preview':
			ksfViews.loadPreview( urlVals.length > 1 ? urlVals[1] : '' );
			break;
			
		case 'faq':
			ksfViews.loadFAQ();
			break;
			
		case 'about':
			ksfViews.loadAbout();
			break;
			
		default:
			ksfViews.loadPreview('');
	}
}

ksfViews.refreshAll = function()
{
	ksfProc.loadView();
}

ksfViews.setupDefault = function()
{
	ksfViews.showFilebar(true);
	ksfViews.showToolSelector(true);
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/left/toolselect/', TOOL_SELECTOR );
}

ksfViews.setupSimple = function()
{
	ksfViews.showFilebar(false);
	ksfViews.showToolSelector(false);
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/left/pagenav/', TOOL_SELECTOR );
}

ksfViews.showFilebar = function(show)
{
	if ( show )
	{
		$(".togglefiles").show();
	}
	else
	{
		$(".togglefiles").hide();
		var fl = $("#sidebar");
		fl.css( { marginRight: -fl.outerWidth() } );
	}
}

ksfViews.showToolSelector = function(show)
{
	if ( show )
	{
		$("toolselector-header").show();
	}
	else
	{
		$("toolselector-header").hide();
	}
}

ksfViews.loadPreview = function(filename)
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/main/file' + encodeURIComponent('=' + filename), CONTENT_AREA );
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/right/file_list/', FILE_SELECTOR );
}

ksfViews.loadFAQ = function()
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/main/faq/', CONTENT_AREA );
}

ksfViews.loadAbout = function()
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/main/about/', CONTENT_AREA );
}
