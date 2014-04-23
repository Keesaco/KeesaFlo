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
							   
						var editDiv = ksfFilebar.newEditElem('div', 'dropdown-file-options fopts-closed');
						editDiv.style.display = 'none';
								
						//star
						var starSpan = ksfFilebar.newEditButton( e.starred ? 'glyphicon-star' : 'glyphicon-star-empty', null, 'left-button-container');
						$(starSpan.inner).click( function () { ksfFilebar.starFile(e, starSpan.inner); } );
						editDiv.appendChild(starSpan.outer);
							   
						var nameSpan = ksfFilebar.newEditElem(
							'a', 'filenameedit file-list-link', null,
							(e.friendlyName ? e.friendlyName : e.filename) );
						nameSpan.href = '#!/preview/' + e.filename;
						newElem.appendChild(nameSpan);
							   
						
						//make the entire list item (but not other components - e.g. the cog - within it) clickable to go to the file view
						$(newElem).click(function(event)
							{
								//                                      <3 IE
								var clickTarget = event.target || event.srcElement;
								if (clickTarget == newElem)
								{
									window.location.href = '#!/preview/' + e.filename;
								}
							} );
							   
						//button to drop down/hide file edit buttons
						var editCog = ksfFilebar.newEditElem('a', 'edit-dropdown-button');
						editCog.appendChild( ksfFilebar.newEditElem(
							'span', 'glyphicon glyphicon-cog',
							function()
							{
								var $div = $(editDiv);
								if ( $div.hasClass("fopts-open") )
								{
									$div.switchClass( "fopts-open", "fopts-closed", 150 );
								}
								else
								{
									$div.switchClass( "fopts-closed", "fopts-open", 150 );
								}
							} ) );
						newElem.appendChild(editCog);
						editDiv.style.display = editDiv.style.display == 'none' ? 'block' : 'none';
								
						var confirmSpan = ksfFilebar.newEditElem('span', 'nameedit-confirm left-button-container');
						confirmSpan.style.display = 'none';
						//confirm rename - tick
						var confirmTick = ksfFilebar.newEditElem('span', 'glyphicon glyphicon-ok nameedit-tick');
						confirmSpan.appendChild(confirmTick);
						//cancel rename - cross
						var confirmCross = ksfFilebar.newEditElem('span', 'glyphicon glyphicon-remove nameedit-cross');
						confirmSpan.appendChild(confirmCross);

						$(nameSpan).on('keypress keyup',
							function(event) { ksfFilebar.renameKeyHandle(event, $(confirmTick), $(confirmCross), $(this))});

						newElem.appendChild(editDiv);
						
							
						//colour button
						editDiv.appendChild( ksfFilebar.newEditButton('glyphicon-tint',
							function () { ksfFilebar.recolourClickHandler(e, newElem); }, 'left-button-container').outer );
							   
						//rename buttom
						editDiv.appendChild( ksfFilebar.newEditButton( 'glyphicon-pencil',
							function () { ksfFilebar.editName(newElem, e); }, 'left-button-container' ).outer );
							   
						//delete button
						editDiv.appendChild(ksfFilebar.newEditButton('glyphicon-trash',
							function ()
							{
								bootbox.confirm("Are you sure you want to delete " + (e.friendlyName ? e.friendlyName : e.filename) + "?",
									function (conf)
									{
										if (conf)
										{
											ksfFilebar.deleteFile(e, newElem);
										}
							} ); },
							'delete-button-container' ).outer);
	
							   
						editDiv.appendChild(confirmSpan);

							   //ensures row does not have to resize on animated glyicon grow
							   editDiv.appendChild(ksfFilebar.newEditElem('span', 'filebar-spacer', null, '&nbsp' ));
							
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
 * \param inner
 * \author jmccrea@keesaco.com of Keesaco
 * \return New element
 */
function ksfFilebar_newEditElem(elemType, className, click, inner)
{
	var newElem = document.createElement(elemType);
	newElem.className = className;
	if (inner)
	{
		newElem.innerHTML = inner;
	}
	
	if (click)
	{
		$(newElem).click(click);
	}
	return newElem;
}
ksfFilebar.newEditElem = ksfFilebar_newEditElem;

/**
 * Makes a new element of a give type, class and hooks a click handler (used to simplify filebar generation)
 * \param String glyphClass - this classname is given to the inner section of the button which contains the icon. 'glyphicon' is added automatically so only the second class (e.g. glyphicon-ok') is required
 * \param Function click - this is hooked to handle click events on the element
 * \author jmccrea@keesaco.com of Keesaco
 * \return New button element
 */
function ksfFilebar_newEditButton(glyphClass, click, outerClass)
{
	var outer = ksfFilebar.newEditElem( 'span', 'file-option-button fbtn-off' + (outerClass ? ' ' + outerClass : '') );
	var inner = ksfFilebar.newEditElem( 'span', 'glyphicon ' + glyphClass, click);
	outer.appendChild(inner)
	$(inner).mouseover(function() { $(outer).switchClass( "fbtn-off", "fbtn-on", 150 ); } )
	.mouseout (function() { $(outer).switchClass( "fbtn-on", "fbtn-off", 150 ); } );
	return {'outer' : outer, 'inner' : inner};
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
	ksfFilebar.selectText($link);
}
ksfFilebar.editName = ksfFilebar_editName;

/**
 * Selects the text of a given element. Used for selecting the text in the name edit; since an editable text element is used rather than a text input field a simple .select() cannot be used.
 * \param $element - jQuery elements; the first element will selected
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 * \note This is not included in .editName() for clarity; at some point it may be useful to move it into a different file
 */
function ksfFilebar_selectText($element)
{
    if (window.getSelection)
	{
        var selection = window.getSelection();
        selection.removeAllRanges();
        var newRange = document.createRange();
        newRange.selectNodeContents($element.get(0));
        selection.addRange(newRange);
    }
	else if (document.selection)
	{
        var newRange = document.body.createTextRange();
        newRange.moveToElementText($element.get(0));
        newRange.select();
    }
}
ksfFilebar.selectText = ksfFilebar_selectText;

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
		var newName = $link.text();
		ksfFilebar.renameFile(file, newName);
		file.friendlyName = newName;
	}
	
}
ksfFilebar.doneEditName = ksfFilebar_doneEditName;

/**
 * Displays a prompt for a new colour choice. Moved from main fiebar draw function for clarity.
 * \param File file - the file to recolour
 * \param Element fileDiv - div which displays the file, used to recolour the border
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 */
function ksfFilebar_recolourClickHandler(file, fileDiv)
{
	var colourInput = document.createElement("input");
	colourInput.type = "color";
	var $boxBody = $(bootbox.confirm("Choose a new colour for " + (file.friendlyName ? file.friendlyName : file.filename) + ": ",
		function (confirm)
		{
			if (confirm)
			{
				ksfFilebar.recolourFile(file, colourInput.value.substring(1),
				function ()
				{
					fileDiv.style.borderRightColor = colourInput.value;
				} );
			}
		})).find('.bootbox-body').first();
	$boxBody.append(colourInput);
}
ksfFilebar.recolourClickHandler = ksfFilebar_recolourClickHandler



// TODO: this can probably be refcatored into a single method

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
 * Sends a request to recolour a given file
 * \param File file - file object for file to recolour (used for .filename)
 * \param String newColour - new colour for file
 * \param Function onSuccess - called if the request is successfull
 * \author jmccrea@keesaco.com of Keesaco
 * \return None
 */
function ksfFilebar_recolourFile(file, newColour, onSuccess)
{
	actionObj = [{
				 'action' 		: 'recolour',
				 'filename'		: file.filename,
				 'newcolour'	: newColour
				 }];
	ksfReq.postJSON(ACTION_URI, actionObj, onSuccess);
}
ksfFilebar.recolourFile = ksfFilebar_recolourFile;

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
				$(removeDiv).qtip("destroy");
				$(removeDiv).remove();
			}
		}
	);
}
ksfFilebar.deleteFile = ksfFilebar_deleteFile;