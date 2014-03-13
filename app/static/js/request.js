/*!************************************************************************
** \file app/static/js/request.js
** \brief JavaScript library client-side request layer
** \author jmccrea@keesaco.com of Keesaco
***************************************************************************
** \package app.static.js.request
** \brief Provides a 'low level' request layer for making HTTP requests on behalf of the data layer
** \note this package assumes that jQuery has already been downloaded by the client
**************************************************************************/


/*!************************************************************************
** \fn ksfReq()
** \brief ksfReq constructor used for namespace
** \author jmccrea@keesaco.com of Keesaco
** \note This constructor currently (intentionally) does not have any effect
***************************************************************************/
function ksfReq()
{
}

/*!************************************************************************
** \fn ksfReq.fetch(URI, callback)
** \brief makes an HTTP request for a given URI and calls the given callback with the reseponse
** \param URI - [string] URI to request
** \param callback	- [function] called with response
** \author jmccrea@keesaco.com of Keesaco
***************************************************************************/
ksfReq.fetch = function(URI, callback, failcallback)
{
	$.get(URI, callback).fail(failcallback);
}

