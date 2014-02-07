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

/*!************************************************************************
** \fn ksfProc.copyPageletInto(URI, targetID)
** \brief gets a pagelet and displays its contents in the target container
** \param URI - [string] pagelet URI
** \param targetID - [string] (Should include '#' prefix) ID of the element to show the pagelet in
** \author jmccrea@keesaco.com of Keesaco
***************************************************************************/
function ksfProc.copyPageletInto(URI, targetID)
{
	///get data and do stuff
	ksfData.fetch( 	URI,
					function(response) {
						ksfData.pageletBody(response)
					} );
}