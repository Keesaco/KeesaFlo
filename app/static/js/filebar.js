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
								
						//star
						starSpan = ksfFilebar.newEditButton('span', 'glyphicon ' + (e.starred ? 'glyphicon-star' : 'glyphicon-star-empty'), null);
						$(starSpan).click( function () { ksfFilebar.starFile(e, starSpan); } );
						editDiv.appendChild(starSpan);

						//button to drop down/hide file edit buttons
						newElem.appendChild( ksfFilebar.newEditButton(
							'span', 'glyphicon glyphicon-cog',
							function() { editDiv.style.display = editDiv.style.display == 'none' ? 'block' : 'none'; } ) );
							   
						var nameSpan = ksfFilebar.newEditButton(
							'a', 'filenameedit file-list-link');
						nameSpan.href = '#!/preview/' + e.filename;
						nameSpan.innerHTML = ' ' + (e.friendlyName ? e.friendlyName : e.filename);
						newElem.appendChild(nameSpan);
								
						//delete button
						editDiv.appendChild( ksfFilebar.newEditButton(
							'span', 'glyphicon glyphicon-trash',
							function () { ksfFilebar.deleteFile(e, newElem); }));
							  
						var confirmSpan = ksfFilebar.newEditButton('span', 'nameedit-confirm', null);
						confirmSpan.style.display = 'none';
						//confirm rename - tick
						var confirmTick = ksfFilebar.newEditButton('span', 'glyphicon glyphicon-ok nameedit-tick', null);
						confirmSpan.appendChild(confirmTick);
						//cancel rename - cross
						var confirmCross = ksfFilebar.newEditButton('span', 'glyphicon glyphicon-remove nameedit-cross', null);
						confirmSpan.appendChild(confirmCross);

						$(nameSpan).on('keypress keyup',
							function(event) { ksfFilebar.renameKeyHandle(event, $(confirmTick), $(confirmCross), $(this))});

						newElem.appendChild(editDiv);
						

						editDiv.appendChild( ksfFilebar.newEditButton(
							'span', 'glyphicon glyphicon-pencil',
							function () { ksfFilebar.editName(newElem, e); } ));
							   
						editDiv.appendChild(confirmSpan);
							
						tdiv.append(newElem);
					} );
			}
		} );
	
}
ksfFilebar.update = ksfFilebar_update;

/**
 * Makes a new element of a give type, class and hooks a click handler (used to simplify filebar generation)
 * \param String elemType - the type of element to create
 * \param String className - the class name for the new element
 * \param Function click - this is hooked to handle click events on the element
 * \author jmccrea@keesaco.com of Keesaco
 * \return New element
 */
function ksfFilebar_newEditButton(elemType, className, click)
{
	var newElem = document.createElement(elemType);
	newElem.className = className;
	$(newElem).click(click);
	return newElem;
}
ksfFilebar.newEditButton = ksfFilebar_newEditButton;

/**
 * Makes a filename editable as a single line
 * \param File file - file object for file to rename (used for .filename)
 * \param String newName - the new name for the given file
 * \author jmccrea@keesaco.com of Keesaco
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

/**
 * Handles key events in editable link - moved out of file selector generation for clarity
 * \param Event event - the event which triggered the call
 * \param Element $confirmButton - the click handler is called to confirm edit
 * \param Element $cancelButton - the click handler is called to cancel the rename
 * \param Element $linkElem - the editable link, the text of this element will be validated
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 */
function ksfFilebar_renameKeyHandle(event, $confirmButton, $cancelButton, $linkElem)
{
	//Since the tick and cross buttons have all the information in their click methods, it's easiest to trigger their events
	//Return key
	if (event.which == 13)
	{
		//prevent inserting a line break
		event.preventDefault();
		$confirmButton.trigger('click');
	}
	//Escape key
	else if (event.which == 27)
	{
		$cancelButton.trigger('click');
	}
	else
	{
		//Remove line breaks
		$linkElem.attr('innerHTML', $(this).text().replace(/(\r\n|\n|\r)/gm,""));
	}
}
ksfFilebar.renameKeyHandle = ksfFilebar_renameKeyHandle;

/**
 * Cleans up the file selector and optionally requests a file rename once editing has finished
 * \param Element fileDiv - the div element for the file's row in the file selector
 * \param File file - file object for file to rename (used for .filename)
 * \param String newHref - the link's HREF gets this value
 * \param Bool update - if true a file rename request is sent, otherwise oldText replaces the current link text and no request is sent
 * \param String oldText - old link text - if update is false, this replaces the link's text
 * \author jmccrea@keesaco.com of Keesaco
 * \note If the request is successful, a redraw of the file selector is forced
 * \return None
 */
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
 * Sends a request to star or unstar a given file
 * \param File file - file object for file to modify (used for .filename, .starred)
 * \param Bool star - If true the file is starred, if false the file is unstarred
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 */
function ksfFilebar_starFile(file, starSpan)
{
	actionObj = [{
		'action' 		: file.starred ? 'unstar' : 'star',
		'filename'		: file.filename
	}];
	ksfReq.postJSON(ACTION_URI, actionObj,
		function (reponse)
		{
			if (reponse[0].success)
			{
				file.starred = (!file.starred);
				if (starSpan)
				{
					starSpan.className = 'glyphicon ' + (file.starred ? 'glyphicon-star' : 'glyphicon-star-empty');
				}
			}
		} );
}
ksfFilebar.starFile = ksfFilebar_starFile;

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
 * \param Element removeDiv - file div to be removed on successful deletion - if deletion succeeds, the div is removed from the DOM
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 */
function ksfFilebar_deleteFile(file, removeDiv)
{
	actionObj = [{
		'action' 		: 'delete',
		'filename'		: file.filename
	}];
	ksfReq.postJSON(ACTION_URI, actionObj,
		function (response)
		{
			if (response[0].success)
			{
				$(removeDiv).remove();
			}
		}
	);
}
ksfFilebar.deleteFile = ksfFilebar_deleteFile;