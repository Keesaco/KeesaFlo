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
 * \todo
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
						newElem.href = '#!/preview/' + e.filename;
						if (e.colour)
						{
							newElem.style.borderRight='10px solid #'+e.colour;
						}
							   
						var editDiv = document.createElement('div');
						editDiv.style.display = 'none';
								
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
						nameSpan.innerHTML = ' ' + (e.friendlyName ? e.friendlyName : e.filename);
						newElem.appendChild(nameSpan);
								
						var delSpan = document.createElement('span');
						delSpan.className = 'glyphicon glyphicon-trash';
						$(delSpan).click(function () { ksfFilebar.deleteFile(e); });
						editDiv.appendChild(delSpan);
							   
						newElem.appendChild(editDiv);
							   
						tdiv.append(newElem);
					} );
			}
		} );
	
}
ksfFilebar.update = ksfFilebar_update;


/**
 * Sends a request to rename a given file
 * \param File file - file object for file to rename (used for .filename)
 * \param String newName - the new name for the given file
 * \author jmccrea@keesaco.com of Keesaco
 * \note If the request is successful, a redraw of the file selector is forced
 * \return None
 */
function ksfFilebar_renameFile(file, newName)
{
	actionObj = [{
		'action' 		: 'rename',
		'filename'		: file.filename,
		'newname'		: newName
	}];
	ksfReq.postJSON(ACTION_URI, actionObj,
		function (response)
		{
			ksfViews.makeFileList();
		}
	);
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