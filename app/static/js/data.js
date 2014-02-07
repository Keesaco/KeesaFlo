/*!************************************************************************
** \file app/static/js/data.js
** \brief JavaScript library for the client-side data layer.
** \author jmccrea@keesaco.com of Keesaco
***************************************************************************
** \package app.static.js.data
** \brief Provides methods for data transformation/intermediate processsing before it is passed to the processing layer
**************************************************************************/


/*!************************************************************************
 ** \fn ksfData()
 ** \brief ksfData constructor used for namespace
 ** \author jmccrea@keesaco.com of Keesaco
 ** \note This constructor currently (intentionally) does not have any effect
 ***************************************************************************/
function ksfData()
{
}


/*!************************************************************************
 ** \fn ksfData.pagelet(data)
 ** \brief splits a downloaded pagelet into body and metadata
 ** \param data - downloaded pagelet to be read
 ** \author jmccrea@keesaco.com of Keesaco
 ***************************************************************************/
function ksfProc.copyPageletInto(URI, targetID)
{
	var res;
	res.body = data;
	return res;
}