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
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfData()
{
}


/**
 * splits a downloaded pagelet into body and metadata
 * \tparam Pagelet data - downloaded pagelet to be read
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
 * \tparam String URI - pagelet URI
 * \tparam String targetID - (Should include '#' prefix) ID of the element to show the pagelet in
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfData_copyPageletInto(URI, targetID)
{
	ksfReq.fetch( 	URI,
					function(response)
				  	{
				 		var pagelet = ksfData.pagelet(response);
				 	 	$(targetID).html(pagelet.body);
				  	} );
}
ksfData.copyPageletInto = ksfData_copyPageletInto;


/**
 * gets location after hashbang and splits by slashes
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
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfData_baseUrl()
{
	return location.href.split("#")[0];
}
ksfData.baseUrl = ksfData_baseUrl;
