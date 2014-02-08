/*!************************************************************************
** \file app/static/js/processing.js
** \brief JavaScript library for the client-side processing layer
** \author jmccrea@keesaco.com of Keesaco
***************************************************************************
** \package app.static.js.processing
** \brief Provides methods for modifying data from the data layer for use by the front-end UI
**************************************************************************/

/*!************************************************************************
** \fn ksfProc()
** \brief ksfProc constructor used for namespace
** \author jmccrea@keesaco.com of Keesaco
** \note This constructor currently (intentionally) does not have any effect
***************************************************************************/
function ksfProc()
{
}

ksfProc.CONTENT_AREA = '#appmain';

/*!************************************************************************
 ** \fn ksfProc.loadFile(filename)
 ** \brief Gets file details pagelet and loads it into the main content area
 ** \param filename - [String] name of file to get details of
 ** \author jmccrea@keesaco.com of Keesaco
 ***************************************************************************/
ksfProc.loadFile = function(filename)
{
	ksfData.copyPageletInto(document.location.href + filename, ksfProc.CONTENT_AREA);
}