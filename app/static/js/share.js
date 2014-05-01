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
PERMISSIONS_SOURCE = '/app/data/json/file_permissions/';
PERMISSIONS_ACTION = '/app/data/edit/file_permissions/';

// Feedback types.
FEEDBACK_DANGER = 'alert-danger';

// Permissions list classes.
PS_FULL  = 'list-group-item list-group-item-success';
PS_READ  = 'list-group-item list-group-item-info';
PS_WRITE = 'list-group-item list-group-item-warning';

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
				userList = document.createElement('ul');
				// Iterate through users.
				response.users.forEach(
					function (user)
					{
						if (!user.isMe)
						{
							userList.appendChild(ksfShare.newUserRow(user, file));
							userList.appendChild(document.createElement('br'));
						}
					} );
					$('#shareModal').find('.modal-user-list').first().html(userList);
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
 * Requests a number of permission edits.
 * \param actionObj - object containing permission editing actions.
 * \author rmurley@keesaco.com of Keesaco
 */
function ksfShare_editPermissions(actionObj)
{
	ksfReq.postJSON(
		PERMISSIONS_ACTION,
		actionObj,
		function(response)
		{
			if (response.success)
			{
				console.log(response);
				setTimeout(function() {ksfShare.getPermissions(actionObj.filename)}, 500);
			}
			else
			{
				ksfGraphTools.showFeedback(FEEDBACK_DANGER, 'Permissions editing error:', response.error);
			};
		},
		function(jqxhr, textStatus, error)
		{
			ksfGraphTools.showFeedback(FEEDBACK_DANGER, textStatus, error);
		} )
}
ksfShare.editPermissions = ksfShare_editPermissions;

/**
 * Creates an element containing a row for viewing/editing a user's permissions for a file
 * \param User userInfo - user/permissions information used to create row
 * \param file - actual (not friendly) name of file.
 * \return Element - div element children for displaying/editing data
 * \author jmccrea@keesaco.com of Keesaco
 * \author rmurley@keesaco.com of Keesaco
 */
function ksfShare_newUserRow(userInfo, file)
{
	// Create user row element.
	rowParent = document.createElement('div');
	rowParent.className = 'user-row';

	// Set user row nickname.
	rowParent.innerHTML = ' ' + userInfo.nickname;
	// Get user's active permissions string.
	var activeStr;
	if (userInfo.permissions.fullControl)
	{
		activeStr = 'All';
	}
	else if (userInfo.permissions.write)
	{
		activeStr = 'Edit';
	}
	else if (userInfo.permissions.read)
	{
		activeStr = 'View';
	}
	// Creating mapping of choices to functions.
	var choiceMapping = [
		['None', function()
			{
				var action = {
					filename : file,
					actions : [{
						action 		: 'dropUser',
						userEmail 	: userInfo.email
					}]
				};
				ksfShare.editPermissions(action);
			}],
		['View', function()
			{
				var action = {
					filename : file,
					actions : [{
						action 		: 'editUser',
						userEmail 	: userInfo.email,
						read 		: true,
						write 		: false,
						fullControl : false
					}]
				};
				ksfShare.editPermissions(action);
			}],
		['Edit', function()
			{
				var action = {
					filename : file,
					actions : [{
						action 		: 'editUser',
						userEmail 	: userInfo.email,
						read 		: true,
						write 		: true,
						fullControl : false
					}]
				};
				ksfShare.editPermissions(action);
			}],
		['All',  function()
			{
				var action = {
					filename : file,
					actions : [{
						action 		: 'editUser',
						userEmail 	: userInfo.email,
						read 		: true,
						write 		: true,
						fullControl : true
					}]
				};
				ksfShare.editPermissions(action);
			}]
	]
	// Add dropdown choice.
	$(rowParent).prepend(ksfShare.buildDropdown(activeStr, choiceMapping));

	/* Add listener.
	$(noneId).click(function ()
		{
			var action = {
				filename : file,
				actions : [{
					action 		: 'dropUser',
					userEmail 	: userInfo.email
				}]
			};
			ksfShare.editPermissions(action);
		});
	*/

	return rowParent;
}
ksfShare.newUserRow = ksfShare_newUserRow;

/**
 * Creates a bootstrap dropdown DOM element, with the active option not in the dropdown.
 * \param activeOption - string that is the name of the active option.
 * \param optionList - array of arrays. First element of sub array is a string listing an option, second element is a function to be hooked to the option.
 * \author rmurley@keesaco.com of Keesaco
 */
function ksfShare_buildDropdown(activeOption, optionList)
{
	// Create main button.
	var activeButton = document.createElement('button');
	activeButton.className = 'btn btn-default dropdown-toggle';
	activeButton.setAttribute('data-toggle', 'dropdown');
	activeButton.innerHTML = activeOption;

	// Add dropdown to button.
	var dropdown = document.createElement('span');
	dropdown.className = 'caret';
	$(activeButton).append(dropdown);

	// Create choices.
	var choices = document.createElement('ul');
	choices.className = 'dropdown-menu';
	choices.setAttribute('role', 'menu');

	// Add options to choices, unless option is active.
	optionList.forEach( function(i) {
			// Get option name.
			str = i[0];
			// Check option isn't active then construct choice.
			if (str !== activeOption)
			{
				var option = document.createElement('li');
				var link = document.createElement('a');
				link.setAttribute('href', '#');
				link.setAttribute('id', 'choice-' + str);
				link.innerHTML = str;
				$(option).append(link);
				$(choices).append(option);
				// Get and hook function.
				func = i[1];
				$(link).click(func);
			}
		}
	);

	// Pack into button and return.
	var button = document.createElement('span');
	$(button).append(activeButton);
	$(button).append(choices);
	return button;
}
ksfShare.buildDropdown = ksfShare_buildDropdown;
