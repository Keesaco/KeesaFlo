/*!************************************************************************
 ** \file app/static/js/views.js
 ** \brief JavaScript library for setting up views within the app page
 ** \author jmccrea@keesaco.com of Keesaco
 ***************************************************************************
 ** \package app.static.js.views
 ** \brief Provides methods for modifying data from the data layer for use by the front-end UI
 **************************************************************************/

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
ksfViews.setupView = function(urlVals)
{
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
	//ksfViews.showToolSelector(true);
}

ksfViews.setupSimple = function()
{
	ksfViews.showFilebar(false);
	//ksfViews.showToolSelector(false);
}

ksfViews.showFilebar = function(show)
{
	if ( show )
	{
		$(".togglefiles").show();
		//$("#sidebar").show();//.css( { marginRight: '0px' } );
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
		/// \todo Specify width properly
		$("#sidebar2").css( { width: '' } );
	}
	else
	{
		$("#sidebar2").css( { width: '0px' } );
	}
}

ksfViews.loadPreview = function(filename)
{
	ksfData.copyPageletInto( ksfData.baseUrl() + encodeURIComponent('file=' + filename), CONTENT_AREA );
	ksfData.copyPageletInto( ksfData.baseUrl() + 'file_list/', FILE_SELECTOR );
}

ksfViews.loadFAQ = function()
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'faq/', CONTENT_AREA );
}

ksfViews.loadAbout = function()
{
	ksfData.copyPageletInto( ksfData.baseUrl() + 'about/', CONTENT_AREA );
}
