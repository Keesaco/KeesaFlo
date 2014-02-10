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
ksfData.pagelet = function(data)
{
	var res = new Array();
	res['body'] = data;
	return res;
}

/*!************************************************************************
 ** \fn ksfData.copyPageletInto(URI, targetID)
 ** \brief gets a pagelet and displays its contents in the target container
 ** \param URI - [string] pagelet URI
 ** \param targetID - [string] (Should include '#' prefix) ID of the element to show the pagelet in
 ** \author jmccrea@keesaco.com of Keesaco
 ***************************************************************************/
ksfData.copyPageletInto = function(URI, targetID)
{
	ksfReq.fetch( 	URI,
					function(response)
				  	{
				 		var pagelet = ksfData.pagelet(response);
				 	 	$(targetID).html(pagelet.body);
				  	} );
}

/*!************************************************************************
 ** \fn ksfData.urlValues()
 ** \brief gets location after hashbang and splits by slashes
 ** \author jmccrea@keesaco.com of Keesaco
 ***************************************************************************/
ksfData.urlValues = function()
{
	var url = location.href
	url = url.split("#!/");
	if (url.length > 1)
	{
		return url[1].split("/");
	}
	else
	{
		return "";
	}
}

/*!************************************************************************
** \fn ksfData.baseUrl()
** \brief gets the part of the URL sent to the server (app base URL)
** \author jmccrea@keesaco.com of Keesaco
***************************************************************************/
ksfData.baseUrl = function()
{
	return location.href.split("/#!/")[0];
}