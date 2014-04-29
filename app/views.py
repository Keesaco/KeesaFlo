###########################################################################
## \file app/views.py
## \brief Generates the pages to be sent to the client using templates files
## \author mrudelle@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
## \author jmccrea@keesaco.com
## \author hdoughty@keesaco.com of Keesaco
###########################################################################

from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import simplejson
from django import forms
import forms
from django.core.files.uploadhandler import FileUploadHandler
from django.core.urlresolvers import reverse
import upload_handling
import API.APIDatastore as ds
import API.PALUsers as auth
import API.APIQueue as queue
import API.APIInstance as instances
import API.APIBackground as background
import API.APIPermissions as ps
import API.APILogging as logging
import json
import re
import gating.tools as gt

DATA_BUCKET = '/fc-raw-data'
GRAPH_BUCKET = '/fc-vis-data'
INFO_BUCKET = '/fc-info-data'

def login(request):
	link = auth.create_login_url('app/')
	return redirect(link)
	
def logout(request):
	link = auth.create_logout_url('/')
	return redirect(link)

###########################################################################
## \brief	Redirects the user to a login page if required, if not
##			redirects to the signup page
## \param	request - Django request which resulted in the call
## \return	HttpResponse - response to the request as JSON
## \author	jmccrea@kessaco.com of Keesaco
###########################################################################
def signup(request):
	link = auth.create_login_url('/#!/signup')
	return redirect(link)

###########################################################################
## \brief	Returns a JSON response which instructs the client to redirect
##			to the landing page
## \return 	HTTPResponse - JSON encoded NotLoggedIn error
## \author	jmccrea@keesaco.com of Keesaco
###########################################################################
def __unauthed_response():
	return HttpResponse(json.dumps({'error' : 'NotLoggedIn'}), content_type="application/json")


###########################################################################
## \brief	Returns a response which instructs the client to redirect to
##			the app's landing page if the user is not logged in.
## \author 	jmccrea@keesaco.com of Keesaco
## \note	At this point the client and server sides do no communicate
##			with JSON consistently. For this reason there is no defined way
##			to inform the CS of an error. At some point it may be useful to
##			define the protocol to allow redirection rather than this being
##			a special case response.
## \return 	HttpResponse - unauthenticated request error object if user
##			is not logged in. None otherwise
###########################################################################
def __check_app_access():
	if auth.get_current_user() is None:
		return __unauthed_response()
	else:
		return None


###########################################################################
## \brief Is called when index page is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \return the index page
###########################################################################
def index(request):
	return render(request, 'index.html')

###########################################################################
## \brief Is called when about page is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \return the about page
###########################################################################
def about(request):
	return render(request, 'about.html')

###########################################################################
## \brief Is called when the F.A.Q page is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \return the F.A.Q page
###########################################################################
def faq(request):
	return render(request, 'faq.html')

###########################################################################
## \brief Is called when the main app page is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \note only the structure of the page is generated here, to fetch the other elements of the page, file_list and file_page should be requested too
## \return the app page skeleton
###########################################################################
def app(request):
	lst = ds.list(DATA_BUCKET)
	file_info = None
	authed_user = auth.get_current_user()

	if authed_user is None:
		return redirect('/')
	else:
		authed_user_nick = authed_user.nickname()

	request.upload_handlers = [upload_handling.fcsUploadHandler()]
	if request.method == 'POST':
		form = forms.UploadFile(request.POST, request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			return redirect('#!/preview/' + request.FILES['file'].name)
		else:
			return render(request, 'app.html', {'form': form, 'files' : lst , 'current_file' : file_info, 'authed_user_nick' : authed_user_nick})
	else:
		form = forms.UploadFile()
		return render(request, 'app.html', {'form': form, 'files' : lst , 'current_file' : file_info, 'authed_user_nick' : authed_user_nick})

###########################################################################
## \brief Is called when the pagelet containing the file list is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \note only the file list is generated here, see app(request) for fetching the page's skeleton
## \return the list of files pagelet
## \todo	Replaced by JSON; remove?
###########################################################################
def file_list(request):
	app_access = __check_app_access()
	if app_access is not None:
		return app_access
	
	lst = ds.list(DATA_BUCKET)

	file_list = []
	
	for temp_file in lst:
		list_entry = {}
		file_entry = permissions.get_file_by_name(temp_file.filename)
		if file_entry is not None:
			list_entry.update({ 'permissions' : 'yes' })
		else:
			list_entry.update({ 'permissions' : 'no'  })
		
		temp_file.filename = temp_file.filename.rpartition('/')[2]
		list_entry.update( { 'filestat' : temp_file } )

		file_list.append(list_entry)

	return render(request, 'file_list.html', {'files' : file_list})

###########################################################################
## \brief returns a JSON representation of a file list
## \param request - Django variable defining the request that triggered the generation of this page
## \todo move 'no files' link markup somewhere else
## \return the list of files pagelet
###########################################################################
def file_list_json(request):
	app_access = __check_app_access()
	if app_access is not None:
		return app_access
	
	authed_user = auth.get_current_user()
	user_key = ps.get_user_key_by_id(authed_user.user_id())
	#TODO: This shouldn't be here - a generic method in APIPermissions would be nice.


	# 'your files'
	file_list = []

	lst = ps.get_user_permissions_list(user_key)
	temp_group = []
	if lst is not None:
		for perm in lst:
			list_entry = {}
			file_entry = ps.get_file_by_key(perm.file_key)
			if file_entry is not None:
				
				temp_file = ds.get_file_info(file_entry.file_name)
				if temp_file is None:
					continue
				
				list_entry.update({ 'permissions' 	: 'yes',
									'friendlyName'	: file_entry.friendly_name,
									'colour'		: perm.colour,
									'starred'		: perm.starred
								} )
		
				temp_file.filename = temp_file.filename.rpartition('/')[2]
				list_entry.update( {	'filename' 		: temp_file.filename,
										'size' 			: temp_file.st_size,
								  		'hash' 			: temp_file.etag,
								  		'timestamp' 	: temp_file.st_ctime
								  })
				temp_group.append(list_entry)


	if len(temp_group) > 0:
		file_list.append({	'catagory' 	: 'owned',
							'heading' 	: 'Your Files',
						 	'type'		: 'files',
							'data' 		: temp_group })
						
	if len(file_list) == 0:
		file_list.append({	'catagory' 	: 'notice',
						 	'type'		: 'html',
						 
						 	# TODO: move this line out
						 	'data'		: '<a data-toggle="modal" data-target="#uploadModal" class="list-group-item">No files - Click here to upload one</a>'
							})


	return HttpResponse(json.dumps(file_list), content_type="application/json")


###########################################################################
## \brief 	Takes a JSON file list edit object and performs the requested
##			action on the specified file. Returns JSON status.
## \param 	request - Django variable defining the request that triggered
##			the generation of this page
## \todo 	Review permissions in this section - correct checking here is
##			vital as edit actions are potentially destructive.
## \todo	Refactor bucket names for deletion
## \todo	Massive refactor is planned
## \return 	JSON response which indicates whether the requested action(s)
##			were performed successfully.
###########################################################################
def file_list_edit(request):
	authed_user = auth.get_current_user()
	if authed_user is None:
		return __unauthed_response()
	
	user_key = ps.get_user_key_by_id(authed_user.user_id())
	
	try:
		actions = json.loads(request.raw_post_data)
	except ValueError:
		return HttpResponse(json.dumps({'error' : 'invalid request payload'}), content_type="application/json")
	
	if not isinstance(actions, list):
		return HttpResponse(json.dumps({'error' : 'Payload is not a list'}), content_type="application/json")
	
	res = []
	for a in actions:
		
		#We can't do anything without a filename
		if 'filename' not in a:
			continue
		else:
			filename = a['filename']
		
		if 'action' not in a:
			continue
		else:
			action = a['action']
		
		res_fragment = {
			'filename' 	: a['filename'],
			'action'	: a['action']
		}
		
		if action == 'delete':
			file_entry = ps.get_file_by_name('/fc-raw-data/' + filename)
			if file_entry is not None:
				ps.remove_file_by_key(file_entry.key)
			
			ds.delete('/fc-raw-data/' + filename)
			ds.delete('/fc-info-data/' + filename + 'info.txt')
			ds.delete('/fc-info-data/' + filename + '.html')
			ds.delete('/fc-vis-data/' + filename + '.png')
			
			res_fragment.update( { 'success' : True } )
		
		#Reinstate this when CE PAL is available
		#else:
		#res_fragment.update( { 'success' : False, 'error' : 'File does not exist.' } )
		
		elif action == 'rename':
			if 'newname' not in a:
				res_fragment.update( { 'success' : False, 'error' : 'New name not specified' } )
			else:
				file_entry = ps.get_file_by_name('/fc-raw-data/' + filename)
				if file_entry is None:
					res_fragment.update( { 'success' : False, 'error' : 'File does not exist.' } )
				else:
					file_entry.friendly_name = a['newname']
					if ps.update_file(file_entry):
						res_fragment.update( { 'success' : True } )
					else:
						res_fragment.update( { 'success' : False, 'error' : 'Could not rename file' } )
		
		elif action == 'star' or action == 'unstar':
			file_entry = ps.get_file_by_name('/fc-raw-data/' + filename)
			if file_entry is None:
				res_fragment.update( { 'success' : False, 'error' : 'File does not exist.' } )
			else:
				fp_entry = ps.get_user_file_permissions(file_entry.key, user_key)
				if fp_entry is None:
					res_fragment.update( { 'success' : False, 'error' : 'Permissions entry not found' } )
				else:
					if ps.modify_file_permissions_by_key(fp_entry.key, new_starred = (action == 'star')):
						res_fragment.update( { 'success' : True } )
					else:
						res_fragment.update( { 'success' : False, 'error' : 'Could not update file' } )

		elif action == 'recolour':
			if 'newcolour' not in a:
				res_fragment.update( { 'success' : False, 'error' : 'New colour not specified' } )
			else:
				colour = a['newcolour']
				chk_string = re.compile("^[A-Fa-f0-9]{6}$")
				if (chk_string.match(colour)):
					file_entry = ps.get_file_by_name('/fc-raw-data/' + filename)
					if file_entry is None:
						res_fragment.update( { 'success' : False, 'error' : 'File does not exist.' } )
					else:
						fp_entry = ps.get_user_file_permissions(file_entry.key, user_key)
						if fp_entry is None:
							res_fragment.update( { 'success' : False, 'error' : 'Permissions entry not found' } )
						else:
							if ps.modify_file_permissions_by_key(fp_entry.key, new_colour = colour):
								res_fragment.update( { 'success' : True } )
							else:
								res_fragment.update( { 'success' : False, 'error' : 'Could not update file' } )
				else:
					res_fragment.update( { 'success' : False, 'error' : 'New colour invalid' } )

		else:
			res_fragment.update( { 'success' : False, 'error' : 'Action not recognised' } )
		
		res.append(res_fragment)
	
	return HttpResponse(json.dumps(res), content_type="application/json")


###########################################################################
## \brief 	Takes a JSON object with a filename and returns a JSON object
##			listing permissions for that file.
## \param 	request - Django variable defining the request that triggered
##			the generation of this data
## \return 	JSON response which indicates whether the requested was
##			successful and if so a lists permissions for the given file.
## \todo	Massive refactor planned - move error checking etc. into lib
## \todo	Enfore full_control as a requirement to use this. Depends on
##			review of permissions use.
## \author	jmccrea@keesaco.com of Keesaco
###########################################################################
def file_permissions_json(request):
	authed_user = auth.get_current_user()
	if authed_user is None:
		return __unauthed_response()
	
	user_key = ps.get_user_key_by_id(authed_user.user_id())

	json_response = {
		'success' 		: False,
		'users'			: []
	}

	try:
		list_req = json.loads(request.raw_post_data)
	except ValueError:
		json_response.update({'error' : 'Invalid request payload.'})
		return HttpResponse(json.dumps(json_response), content_type="application/json")

	if 'filename' not in list_req:
		json_response.update({'error' : 'Incomplete request.'})
		return HttpResponse(json.dumps(json_response), content_type="application/json")

	filename = list_req['filename']

	file_entry = ps.get_file_by_name('/fc-raw-data/' + filename)
	if file_entry is None:
		json_response.update( { 'error' : 'File does not exist.' } )
		return HttpResponse(json.dumps(json_response), content_type="application/json")
		
	fp_entry = ps.get_user_file_permissions(file_entry.key, user_key)
	if fp_entry is None:
		json_response.update( { 'error' : 'Permission denied.' } )
		return HttpResponse(json.dumps(json_response), content_type="application/json")

	permissions_list = ps.get_file_permissions_list(file_entry.key)
	if permissions_list is None:
		json_response.update( { 'error' : 'Permission could not be retrieved.' } )
		return HttpResponse(json.dumps(json_response), content_type="application/json")

	for perm in permissions_list:
		new_perm = {}
		user = ps.get_user_by_key(perm.user_key)
		if user is not None:
			nickname = user.nickname()
			email = user.email()
			user_found = True
		else:
			nickname = 'Unknown'
			email = 'unknown'
			user_found = False

		new_perm.update( {
			'nickname' 		: nickname,
			'userFound'		: user_found,
			'email'			: email,
			'isMe'			: (perm.user_key == user_key),
			'permissions'	: {
				'read'			: perm.read,
				'write'			: perm.write,
				'fullControl'	: perm.full_control
			}
		} )

		json_response['users'].append(new_perm)

	json_response.update({ 'success' : True })
	return HttpResponse(json.dumps(json_response), content_type="application/json")


###########################################################################
## \brief Is called when the pagelet containing the main content of the page is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param file - define which file has to be rendered
## \note only the main panel is generated here, see app(request) for fetching the page's skeleton
## \return the app main panel
###########################################################################
def file_preview(request, file = None):
	app_access = __check_app_access()
	if app_access is not None:
		return app_access

	## Authentication.
	authed_user = auth.get_current_user()
	if authed_user is None:
		authed_user_nick = 'Guest'
	else:
		authed_user_nick = authed_user.nickname()
	## Graph visualisation.
	# Replaced by a spinning canvas on the clientside
	# if not ds.check_exists(GRAPH_BUCKET + '/' + file_name_without_extension + '.png', None):
	# 	file_name_without_extension = None

	#TODO: Might need to be simplified or moved to a function in fileinfo
	# TODO the folowing should be replaced by a method in the APIDatastore
	file_info = ps.get_file_by_name(DATA_BUCKET + '/' + file)

	undo_uri = None
	if file_info is not None:
		prev_file = ps.get_file_by_key(file_info.prev_file_key)
		if prev_file is not None:
			undo_uri = prev_file.file_name.rpartition(DATA_BUCKET + '/')[2]

	lst = ds.list(DATA_BUCKET)
	current_file = None
	for temp_file in lst:
		temp_file.filename = temp_file.filename.rpartition('/')[2]
		if temp_file.filename == file:
			current_file = temp_file;

	# Check whether graph exists yet.
	graph_exists = ds.check_exists(GRAPH_BUCKET + '/' + file.partition('.')[0] + '.png', None)

	# Get permissions for file.
	user_key = ps.get_user_key_by_id(authed_user.user_id())
	permissions = ps.get_user_file_permissions(file_info.key, user_key)

	return render(request, 'file_preview.html', {'current_file' : current_file,
												 'name' : file,
												 'authed_user_nick': authed_user_nick,
												 'file_info' : file_info,
				 								 'graph_ready' : graph_exists,
				  								 'undo_link' : undo_uri,
				  								 'permissions' : permissions })

###########################################################################
## \brief 	view for graph preview pagelet
## \param 	request - Django variable defining the request that triggered
##			the generation of this page
## \note 	only the main panel is generated here, see app(request) for
##			fetching the page's skeleton
## \return 	the main panel pagelet
## \todo	use datastore/permissions API for file list lookup
## \todo	check permissions, return HTTP error on failure
###########################################################################
def graph_preview(request, file = None):
	lst = ds.list(DATA_BUCKET)
	for temp_file in lst:
		temp_file.filename = temp_file.filename.rpartition('/')[2]
		if temp_file.filename == file:
			file_info = temp_file;

	return render(request, 'graph_preview.html',
		{'current_file' : file_info, 'file_name_without_extension' : file})

###########################################################################
## \brief Is called when the pagelet containing the app's main panel is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \note only the main panel is generated here, see app(request) for fetching the page's skeleton
## \return the main panel pagelet
###########################################################################
'''
def file_page(request, file=None):
	app_access = __check_app_access()
	if app_access is not None:
		return app_access
	
	lst = ds.list('/fc-raw-data')
	file_info = None
	for temp_file in lst:
		temp_file.filename = temp_file.filename.rpartition('/')[2]
		if temp_file.filename == file:
			file_info = temp_file;
	return render(request, 'file_preview.html', {'current_file' : file_info, 'authed_user_nick': authed_user_nick, 'file_name_without_extension' : file_name_without_extension})
'''

def pagenav(request):
	return render(request, 'pagenav.html')

def toolselect(request):
	return render(request, 'toolselect.html')

###########################################################################
## \brief Is called when a graph is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param graph - name of the graph (without the extension .png)
## \return the graph's immage
###########################################################################
def get_graph(request, graph):
	return fetch_file(GRAPH_BUCKET + '/' + graph + ".png", 'image/png', False)

###########################################################################
## \brief Is called when a file is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param dataset - the name of the dataset to be downloaded
## \return the file requested
###########################################################################
def get_dataset(request, dataset):
	return fetch_file(DATA_BUCKET + '/' + dataset + '.fcs', 'application/vnd.isac.fcs', True)

###########################################################################
## \brief Is called when a info is requested
## \param request - Django variable defining the request that triggered the generation of this page
## \param dataset - the name of the file to be downloaded
## \return the file requested
###########################################################################
def get_info(request, infofile):
	return fetch_file(INFO_BUCKET + '/' + infofile, 'text/html', False)

###########################################################################
## \brief Return a response containing the file
## \param path - path to the file to be sent to the client
## \param type - type of the file sent (its mime type)
## \param friendly - boolean indicating if fetch as friendly name.
## \return an HttpResponse ccontaining the file to be sent
###########################################################################
def fetch_file(path, type, friendly):
	# TODO: Need protection against hack such as ../
	buffer = ds.open(path)
	if buffer:
		file = buffer.read()
		# TODO: Maybe transform the httpresponse to streaminghttpresponse in case the graph is really large and to improve efficiency
		response = HttpResponse(file, content_type=type)
		# Get filename.
		if friendly:
			path = path.rpartition('/')[0] + '/' + ps.get_file_by_name(path).friendly_name
		# Construct and send response
		response['Content-Disposition'] = 'attachment; filename="' + path + '"'
		return response
	else:
		return HttpResponseNotFound('<h1>404 : ' + path + ' not found</h1>')

###########################################################################
## \brief Is called when the settings page is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \return the settings page
###########################################################################
def settings(request):
	app_access = __check_app_access()
	if app_access is not None:
		return app_access
	
	return render(request, 'settings.html')

###########################################################################
## \brief Is called by a tool from the client side
## \param request - Django variable defining the request that triggered the generation of this page
## \return a JSON object in a httpresponse, containing the status of the gating, a short message and the link to the newly created graph
## \todo Tidy up validation
###########################################################################
def tool(request):
	authed_user = auth.get_current_user()
	if authed_user is None:
		return __unauthed_response()


	try:
		gate_info = json.loads(request.raw_post_data)
		print gate_info
	except ValueError:
		return HttpResponse(simplejson.dumps(gt.generate_gating_feedback('fail', 'Invalid request payload')), content_type="application/json")


	## \todo This should probably iterate over list
	if (('points' 	not in gate_info) or
		('tool'		not in gate_info) or
		('filename' not in gate_info)):

		return HttpResponse(simplejson.dumps(gt.generate_gating_feedback('fail', 'Incomplete gate parameters')), content_type="application/json")

	if (gate_info['points']):
		if not isinstance(gate_info['points'], list):
			return HttpResponse(simplejson.dumps(gt.generate_gating_feedback('fail', 'Invalid points list')), content_type="application/json")
	else:
		# Normalise false value to None
		gateInfo.update( { 'points' : None } )


	tool = gt.AVAILABLE_TOOLS.get(gate_info['tool'], gt.no_such_tool)
	## first two arguments passed for compatibility
	tool_response = tool(gate_info)

	## Load balance instances in the background.
	background.run(instances.balance, 0)

	json_response = simplejson.dumps(tool_response);
	return HttpResponse(json_response, content_type="application/json")

###########################################################################
## \brief	Returns a JSON object representing the analysis status of a
##			given file.
## \param	request - Django request which resulted in the call
## \return	HttpResponse - response to the request as JSON
## \author	jmccrea@kessaco.com of Keesaco
## \todo	Consider permissions update after CE/Permissions integration
## \todo	Refactor return value creation
###########################################################################
def analysis_status_json(request):
	authed_user = auth.get_current_user()
	if authed_user is None:
		return __unauthed_response()

	user_key = ps.get_user_key_by_id(authed_user.user_id())

	response_part = {
		'backoff' 	: 0,		#tells the client to back off for a given amount of time (milliseconds) (This is added to the client's constant poll interval)
		'giveup'	: True,		#True instructs the client to stop polling - useful for situations such as unauthed requests where polling will never result in the user being shown a graph
		'done'		: False		#True indicates that the analysis has finished and that the user can be redirected to the new image
	}
	
	try:
		file_req = json.loads(request.raw_post_data)
	except ValueError:
		response_part.update({'error' : 'Invalid request payload.'})
		return HttpResponse(json.dumps(response_part), content_type="application/json")

	if 'filename' not in file_req:
		response_part.update({'error' : 'Incomplete request.'})
		return HttpResponse(json.dumps(response_part), content_type="application/json")

	#	This is roughly what permissions checking should probably look like once all files have permissions entries
	#		Alternatively, a check_exists call may be sufficient if the permissions entry is created before gating is requested,
	#		this will depend on the CE/Permissions integration method
	file_entry = ps.get_file_by_name(file_req['filename'])
	if file_entry is None:
		response_part.update( { 'error' : 'File or gate not recognised.', 'giveup' : False } )
		return HttpResponse(json.dumps(response_part), content_type="application/json")
	else:
		fp_entry = ps.get_user_file_permissions(file_entry.key, user_key)
		if fp_entry is None:
			response_part.update( { 'error' : 'Permission denied.' } )
			return HttpResponse(json.dumps(response_part), content_type="application/json")

	name = file_req['filename'].rpartition('/')[2]
	is_done =  ds.check_exists(GRAPH_BUCKET + '/' + name + '.png', None)

	#Prevent redirecting before the view is ready
	is_done &= ds.check_exists(DATA_BUCKET  + '/' + name, None)

	response_part.update( { 'done' : is_done, 'giveup' : False } )
	return HttpResponse(json.dumps(response_part), content_type="application/json")

###########################################################################
## \brief	Gives the user canLogIn and returns a JSON success/error object
## \param	request - Django request which resulted in the call
## \return	HttpResponse - response to the request as JSON
## \author	jmccrea@kessaco.com of Keesaco
## \note	Currently signup gives a user permissions and nothing else for
##			the purpose of demonstration. Ultimately the validation,
##			storage and response will need a number of additions.
###########################################################################
def signup_handler(request):
	authed_user = auth.get_current_user()
	if authed_user is None:
		return __unauthed_response()

	user_key = ps.get_user_key_by_id(authed_user.user_id())
	if user_key is None:
		user_key = ps.add_user(authed_user)

	response_part = {
		'success'		: False
	}

	try:
		file_req = json.loads(request.raw_post_data)
	except ValueError:
		response_part.update({'error' : 'Invalid request payload.'})
		return HttpResponse(json.dumps(response_part), content_type="application/json")
		
	if 'action' not in file_req:
		response_part.update({'error' : 'Incomplete request.'})
		return HttpResponse(json.dumps(response_part), content_type="application/json")

	elem_key = ps.get_element_key_by_ref('canLogIn')
	if elem_key is None:
		elem_key = ps.add_element('canLogIn')

	user_elem = ps.get_user_element_permissions(user_key, elem_key)
	if user_elem is not None:
		response_part.update({'error' : 'Already signed up.'})
		return HttpResponse(json.dumps(response_part), content_type="application/json")
	else:
		ps.add_element_permissions(user_key, elem_key, True)

		response_part.update({'success' : True})
		return HttpResponse(json.dumps(response_part), content_type="application/json")
