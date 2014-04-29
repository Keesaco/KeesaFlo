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
 * Gets permissions for a file, enabling share button is active user has full control.
 * \param file - actual (not friendly) name of file.
 * \author rmurley@keesaco.com of Keesaco
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
					console.log(response);
					// Iterate through users.
					for (var i = 0; i < response.users.length; i++) {
						// If active user has full control, enable share button.
						if (response.users[i].isMe && response.users[i].permissions.fullControl)
						{
							ksfCanvas.enableBtn(SHARE_BTN, true);
						}
					}
				}
				else
				{
					ksfGraphTools.showFeedback(FEEDBACK_DANGER, 'Permissions error:', 'Unsuccessful request');
				}
			},
		function(jqxhr, textStatus, error)
			{
				ksfGraphTools.showFeedback(FEEDBACK_DANGER, textStatus, error);
			})
}
ksfShare.getPermissions = ksfShare_getPermissions;
