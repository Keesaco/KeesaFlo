/**
 * \file app/static/js/processing.js
 * \brief JavaScript library for the client-side processing layer
 * \author jmccrea@keesaco.com of Keesaco
 */

/**
 * \package app.static.js.processing
 * \brief Provides methods for modifying data from the data layer for use by the front-end UI
 */


/**
 * ksfProc constructor used for namespace
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfProc()
{
}


/**
 * ksfProc.loadFile(filename)
 * Gets file details pagelet and loads it into the main content area
 * \tparam String filename - name of file to get details of
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfProc_loadFile(filename)
{
	ksfData.copyPageletInto(document.location.href + filename, ksfProc.CONTENT_AREA);
}
ksfProc.loadFile = ksfProc_loadFile;
