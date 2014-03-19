/**
 * \file app/static/js/request.js
 * \brief JavaScript library client-side request layer
 * \author jmccrea@keesaco.com of Keesaco
 */

/** 
 * \package app.static.js.request
 * \brief Provides a 'low level' request layer for making HTTP requests on behalf of the data layer
 * \note this package assumes that jQuery has already been downloaded by the client
 */


/**
 * ksfReq constructor used for namespace
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfReq()
{
}


/**
 * makes an HTTP request for a given URI and calls the given callback with the reseponse
 * \param String URI - URI to request
 * \param Function callback - called with received data after a response is received
 * \param Function failcallback - called on request failure
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfReq_fetch(URI, callback, failcallback)
{
	$.get(URI, callback).fail(failcallback);
}
ksfReq.fetch = ksfReq_fetch;
