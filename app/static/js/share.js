/**
 * \file app/static/js/share.js
 * \brief JavaScript library for sharing fcs files.
 * \author rmurley@keesaco.com of Keesaco
 */

/** 
 * \package app.static.js.share
 * \brief Provides methods for sharing fcs files.
 */


/**
 * ksfShare constructor used for namespace
 * \return None
 * \author rmurley@keesaco.com of Keesaco
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfShare(){
}

// Fetch share button from DOM.
SHARE_BTN = "#share-btn";

// Data sources.
PERMISSIONS_SOURCE = '/app/data/json/file_permissions_json';

// Feedback types.
FEEDBACK_DANGER = "alert-danger";

/**
 * Gets permissions for a file.
 * \param file - actual (not friendly) name of file.
 * \author rmurley@keesaco.com of Keesaco
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfShare_getPermissions(file)
{
	ksfReq.postJSON(
		PERMISSIONS_SOURCE,
		{filename : file},
		function(response)
		{
			if (response.success)
			{
				userList = document.createElement('div');
					
				// Iterate through users.
				response.users.forEach(
					function (user)
					{
						if (!user.isMe)
						{
							userList.appendChild(ksfShare.newUserRow(user));
						}
					} );
					$('#shareModal').find('.modal-body').first().html(userList);
			}
			else
			{
				ksfGraphTools.showFeedback(FEEDBACK_DANGER, 'Permissions error:', response.error);
			}
		},
		function(jqxhr, textStatus, error)
		{
			ksfGraphTools.showFeedback(FEEDBACK_DANGER, textStatus, error);
		} )
}
ksfShare.getPermissions = ksfShare_getPermissions;

/**
 * Creates an element containing a row for viewing/editing a user's permissions for a file
 * \param User userInfo - user/permissions information used to create row
 * \return Element - div element children for displaying/editing data
 * \author jmccrea@keesaco.com of Keesaco
 */
function ksfShare_newUserRow(userInfo)
{
	rowParent = document.createElement('div');
	rowParent.innerHTML = userInfo.nickname;
	
	return rowParent;
}
ksfShare.newUserRow = ksfShare_newUserRow;
