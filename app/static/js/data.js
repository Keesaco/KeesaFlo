/**
 * \file app/static/js/data.js
 * \brief JavaScript library for the client-side data layer.
 * \author jmccrea@keesaco.com of Keesaco
 */

/** \package app.static.js.data
 * \brief Provides methods for data transformation/intermediate processsing before it is passed to the processing layer
 */


/**
 * ksfData constructor used for namespace
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfData()
{
}


/**
 * splits a downloaded pagelet into body and metadata
 * \tparam Pagelet data - downloaded pagelet to be read
 * \treturn Object pagelet with body property containing page data
 * \note This currently serves little purpose but allows for future inclusion of metadata with pagelets
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfData_pagelet(data)
{
	var res = new Array();
	res['body'] = data;
	return res;
}
ksfData.pagelet = ksfData_pagelet;


/**
 * gets a pagelet and displays its contents in the target container
 * \param String URI - pagelet URI
 * \param String targetID - (Should include '#' prefix) ID of the element to show the pagelet in
 * \param Function executeOnLoading - To be executed once the pagelet is completely loaded in the page
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfData_copyPageletInto(URI, targetID, executeOnLoading)
{
	ksfReq.fetch( 	URI,
					function(response)
				  	{
				 		var pagelet = ksfData.pagelet(response);
				 	 	$(targetID).html(pagelet.body);
				 	 	if (executeOnLoading) {
				 	 		executeOnLoading();
				 	 	}
				  	} );
}
ksfData.copyPageletInto = ksfData_copyPageletInto;


/**
 * gets location after hashbang and splits by slashes
 * \treturn String[] An array of values on the RHS of the hashbang in the URL, values are split by '/'
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfData_urlValues()
{
	var hash = location.hash.split('#!/');
	if (hash.length > 1)
	{
		return hash[1].split('/');
	}
	else
	{
		return null;
	}
}
ksfData.urlValues = ksfData_urlValues;


/**
 * gets the part of the URL sent to the server (app base URL)
 * \treturn String The base-URL of the application (part preceding the hashbang)
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfData_baseUrl()
{
	return location.href.split("#")[0];
}
ksfData.baseUrl = ksfData_baseUrl;

/**
 * Makes an asynchronous request for JSON formatted data - wrapper around ksfData method
 * \param String URI - URI to request
 * \param Function callback - called with received data
 * \param Function failcallback - called if the request fails
 * \return return value of ksfReq.fetchJSON - currently None
 * \note This method is purely a wrapper around the method of the same name in ksfReq
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfData_fetchJSON(URI, callback, failcallback)
{
	return ksfReq.fetchJSON(URI, callback, failcallback);
}
ksfData.fetchJSON = ksfData_fetchJSON;
