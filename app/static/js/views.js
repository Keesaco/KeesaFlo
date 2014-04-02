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
FILES_AREA = '#filelist';
TOOLS_AREA = '#toolselector';

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
	//invalidate current file information
	ksfViews.currentFile = null;
	ksfViews.currentFileName = null;
	
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
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/left/toolselect/', TOOLS_AREA, ksfTools.addToolsListener );
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
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/left/pagenav/', TOOLS_AREA, null );
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
	ksfViews.currentFileName = filename;
	ksfData.copyPageletInto( ksfData.baseUrl() + 'panels/main/file' + encodeURIComponent('=' + filename), CONTENT_AREA, ksfLayout.filePreviewStart);
	ksfViews.makeFileList('/app/data/json/files/', FILES_AREA);
}
ksfViews.loadPreview = ksfViews_loadPreview;

/**
 * Uses the JSON files source to construct the file selector
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_makeFileList(datasource, target)
{
	ksfData.fetchJSON(datasource,
		function(data)
		{
			//clear out file list
			ksfViews.files = [];
					  
			//destroy old file previews
			$('.file-preview-tip').remove();
			var tdiv = $(target);
			tdiv.empty();
			data.forEach(
				function (d)
				{
					if (d.type == 'html')
					{
						tdiv.append(d.data)
					}
					else if (d.type = 'files')
					{
						d.data.forEach(
							function(e)
							{
								//Add file info to file list
								ksfViews.files.push(e);
								   
								//if it's the currently selected file then store a reference in .currentFile
								if (ksfViews.currentFileName == e.filename && e.filename)
								{
									ksfViews.currentFile = e;
								}
									   
								var newElem = document.createElement('a');
								newElem.className = 'list-group-item file-list-item';
								newElem.href = '#!/preview/' + e.filename;
								newElem.innerHTML = e.filename
								tdiv.append(newElem);
							} );
					}
				} );
	
		} );
}
ksfViews.makeFileList = ksfViews_makeFileList;

/**
 * Searches the most recent file list available and returns a file by a given name if found
 * \param String probe - name of file to search for
 * \return null if not found, otherwise a file information object as defined by the JSON datasource
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfViews_getFileInfoByName(probe)
{
	ksfViews.files.forEach(
		function (file)
		{
			if (file.filename == probe)
			{
				return file;
			}
		} );
	return null;
}
ksfViews.getFileInfoByName = ksfViews_getFileInfoByName;

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
