/**
 * \file app/static/js/views.js
 * \brief JavaScript library for setting up views within the app page
 * \author jmccrea@keesaco.com of Keesaco
 */

/**
 * \package app.static.js.views
 * \brief Provides methods for modifying data from the data layer for use by the front-end UI
 */


/**
 *\fn anonymous_window_onhashchange_views
 *\todo This has limited browser compatibility, if this is an issue support for onhashchange could be checked and an alternative timer arrangement provided for older browsers.
 */
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

/**
 * Sets up the correct view then loads required panels given the current URL
 * \tparam Boolean force - if true the view will be updated even if the URL value is empty
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_loadFromLocation(force)
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
ksfViews.loadFromLocation = ksfViews_loadFromLocation;


/**
 * downloads and displays the correct panels for the current view given the URL
 * \tparam String[] urlVals - values taken from the RHS of the hashbang in the URL if found
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_loadView(urlVals)
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
ksfViews.loadView = ksfViews_loadView;


/**
 * reloads the current view
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_refreshAll()
{
	ksfProc.loadView();
}
ksfViews.refreshAll = ksfViews_refreshAll;


/**
 * sets up the default view (file preview/gating)
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_setupDefault()
{
	ksfLayout.filesButtonShow();
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/left/toolselect/', TOOL_SELECTOR, ksfTools.addToolsListener );
}
ksfViews.setupDefault = ksfViews_setupDefault;


/**
 * sets up the simple view (FAQ/about)
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_setupSimple()
{
	ksfLayout.filesButtonHide();
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/left/pagenav/', TOOL_SELECTOR, null );
}
ksfViews.setupSimple = ksfViews_setupSimple;


/**
 * Downloads and displays the panels for the file preview view
 * \tparam String filename - name of file to show
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_loadPreview(filename)
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/main/file' + encodeURIComponent('=' + filename), CONTENT_AREA, ksfLayout.filePreviewStart);
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/right/file_list/', FILE_SELECTOR_ID, null);
}
ksfViews.loadPreview = ksfViews_loadPreview;


/**
 * Downloads and displays the panels for the FAQ page
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_loadFAQ()
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/main/faq/', CONTENT_AREA, null );
}
ksfViews.loadFAQ = ksfViews_loadFAQ;


/**
 * Downloads and displays the panels for 'about' page
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_loadAbout()
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/main/about/', CONTENT_AREA, null );
}
ksfViews.loadAbout = ksfViews_loadAbout;
