/**
 * \file app/static/js/filebar.js
 * \brief JavaScript for controlling and performing actions on behalf of the file selector. This relies heaivily on views.js, but has been seperated from views.js as its functionality is confined to the file selector.
 * \author jmccrea@keesaco.com of Keesaco
 */

/** \package app.static.js.data
 * \brief Provives methods used when interacting with and displaying the file selector */

FILES_AREA = '#filelist';
ACTION_URI = '/app/data/edit/files/';

/**
 * ksfFilebar constructor used for namespace
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 * \note This constructor currently (intentionally) does not have any effect
 */
function ksfFilebar()
{
}

/**
 * updates the filebar given a file list object
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 * \todo remove checking for permissions entries once CE PAL has been implemented
 * \todo refactor
 */
function ksfFilebar_update(data)
{
	//clear out file list
	ksfViews.files = [];
	
	//destroy old file previews
	$('.file-preview-tip').remove();
	var tdiv = $(FILES_AREA);
	tdiv.empty();
	data.forEach(
		function (d)
		{
			if (d.type == 'html')
			{
				tdiv.append(d.data)
			}
			else if (d.type = 'files')
			{
				d.data.forEach(
					function(e)
					{
						//Add file info to file list
						ksfViews.files.push(e);
								
						//if it's the currently selected file then store a reference in .currentFile
						if (ksfViews.currentFileName == e.filename && e.filename)
						{
							ksfViews.currentFile = e;
						}
								
						var newElem = document.createElement('a');
						newElem.className = 'list-group-item file-list-item';
						if (e.colour)
						{
							newElem.style.borderRight='10px solid #'+e.colour;
						}
							   
						var editDiv = document.createElement('div');
						editDiv.style.display = 'none';
						editDiv.className = 'dropdown-file-options';
								
						//TODO: remove this when permissions are set for all files
						if (e.permissions == 'yes')
						{
							starSpan = document.createElement('span');
							starSpan.className = 'glyphicon ' + (e.starred ? 'glyphicon-star' : 'glyphicon-star-empty');
							editDiv.appendChild(starSpan);
						}

						var editDrop = document.createElement('span');
						$(editDrop).click( function() { editDiv.style.display = editDiv.style.display == 'none' ? 'block' : 'none'; } );
						editDrop.className = 'glyphicon glyphicon-cog';
						newElem.appendChild(editDrop);
							   
						var nameSpan = document.createElement('span');
						nameSpan = document.createElement('a');
						nameSpan.className = 'filenameedit file-list-link'
						nameSpan.href = '#!/preview/' + e.filename;
						nameSpan.innerHTML = ' ' + (e.friendlyName ? e.friendlyName : e.filename);
						newElem.appendChild(nameSpan);
								
						var delSpan = document.createElement('span');
						delSpan.className = 'glyphicon glyphicon-trash';
						$(delSpan).click(function () { ksfFilebar.deleteFile(e); });
						editDiv.appendChild(delSpan);
							   
						var confirmSpan = document.createElement('span');
						confirmSpan.className = 'nameedit-confirm';
						confirmSpan.style.display = 'none';
						var confirmTick = document.createElement('span');
						confirmTick.className = 'glyphicon glyphicon-ok nameedit-tick';
						confirmSpan.appendChild(confirmTick);
						var confirmCross = document.createElement('span');
						confirmCross.className = 'glyphicon glyphicon-remove nameedit-cross';
						confirmSpan.appendChild(confirmCross);

						$(nameSpan).on('keypress keyup',
							function(event)
							{
								//Since the tick and cross buttons have all the information in their click methods, it's easiest to trigger their events
								//Return key
								if (event.which == 13)
								{
									//prevent inserting a line break
									event.preventDefault();
									$(confirmTick).trigger('click');
								}
								//Escape key
								else if (event.which == 27)
								{
									$(confirmCross).trigger('click');
								}
								else
								{
									//Remove line breaks
									$(this).attr('innerHTML', $(this).text().replace(/(\r\n|\n|\r)/gm,""));
								}
							} );
							   

						newElem.appendChild(editDiv);
							   
						renameSpan = document.createElement('span');
						renameSpan.className = 'glyphicon glyphicon-pencil';
						$(renameSpan).click(function () { ksfFilebar.editName(newElem, e); } );
						editDiv.appendChild(renameSpan);
							   
						editDiv.appendChild(confirmSpan);
							
						tdiv.append(newElem);
					} );
			}
		} );
	
}
ksfFilebar.update = ksfFilebar_update;

/**
 * Makes a filename editable as a single line
 * \param File file - file object for file to rename (used for .filename)
 * \param String newName - the new name for the given file
 * \author jmccrea@keesaco.com of Keesaco
 * \note If the request is successful, a redraw of the file selector is forced
 * \return None
 */
function ksfFilebar_editName(fileDiv, file)
{
	var $link = $(fileDiv).children('.filenameedit').first()
	var prevHref = $link.href;
	$link.href = ''
	var oldText = $link.text();
	$link.className = 'filenameedit';
	
	var $confirmSpan = $(fileDiv).children('.dropdown-file-options').children('.nameedit-confirm');
	$confirmSpan.first().css('display', ' inline');
	$confirmSpan.children('.nameedit-tick').click(  function() { ksfFilebar.doneEditName(fileDiv, file, prevHref, true); } );
	$confirmSpan.children('.nameedit-cross').click( function() { ksfFilebar.doneEditName(fileDiv, file, prevHref, false, oldText); } );
	
	$link.attr('contenteditable', 'true');
	$link.trigger('focus');
}
ksfFilebar.editName = ksfFilebar_editName;

function ksfFilebar_doneEditName(fileDiv, file, newHref, update, oldText)
{
	var $link = $(fileDiv).children('.filenameedit').first()
	$link.href = newHref
	$link.attr('contenteditable', 'false');
	$link.className = 'filenameedit file-list-link';
	$link.trigger('blur');
	
	var $confirmSpan = $(fileDiv).children('.dropdown-file-options').children('.nameedit-confirm');
	$confirmSpan.first().css('display', 'none');
	
	if (!update)
	{
		$link.text(oldText);
	}
	else
	{
		ksfFilebar.renameFile(file, $link.text());
	}
	
}
ksfFilebar.doneEditName = ksfFilebar_doneEditName;


/**
 * Sends a request to rename a given file
 * \param File file - file object for file to rename (used for .filename)
 * \param String newName - the new name for the given file
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 */
function ksfFilebar_renameFile(file, newName)
{
	actionObj = [{
		'action' 		: 'rename',
		'filename'		: file.filename,
		'newname'		: newName
	}];
	ksfReq.postJSON(ACTION_URI, actionObj);
}
ksfFilebar.renameFile = ksfFilebar_renameFile;

/**
 * Sends a request to delete a given file
 * \param File file - file object for file to delete (used for .filename)
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 * \note If the request is successful, a redraw of the file selector is forced
 */
function ksfFilebar_deleteFile(file)
{
	actionObj = [{
		'action' 		: 'delete',
		'filename'		: file.filename
	}];
	ksfReq.postJSON(ACTION_URI, actionObj,
		function (response)
		{
			ksfViews.makeFileList();
		}
	);
}
ksfFilebar.deleteFile = ksfFilebar_deleteFile;