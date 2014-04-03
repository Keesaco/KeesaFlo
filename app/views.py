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
import API.APIPermissions as ps
import json

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
###########################################################################
def file_list(request):
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
	lst = ds.list(DATA_BUCKET)
	
	authed_user = auth.get_current_user()
	if authed_user is None:
		pass
		#TODO: deal with unauthed users
	else:
		user_key = ps.get_user_key_by_id(authed_user.user_id())
		#TODO: This shouldn't be here - a generic method in APIPermissions would be nice.


	# 'your files'
	file_list = []
	
	temp_group = []
	for temp_file in lst:
		list_entry = {}
		file_entry = ps.get_file_by_name(temp_file.filename)
		if file_entry is not None:
			user_permissions = ps.get_user_file_permissions(file_entry.key, user_key)
			list_entry.update({ 'permissions' 	: 'yes',
								'friendlyName'	: file_entry.friendly_name,
							  	'colour'		: user_permissions.colour,
							  	'starred'		: user_permissions.starred
							} )
							  
			
		else:
			list_entry.update({ 'permissions' : 'no'  })
		
		
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
## \brief Is called when the pagelet containing the main content of the page is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param file - define which file has to be rendered
## \note only the main panel is generated here, see app(request) for fetching the page's skeleton
## \return the app main panel
###########################################################################
def file_preview(request, file = None):
	## Authentication.
	authed_user = auth.get_current_user()
	if authed_user is None:
		authed_user_nick = 'Guest'
	else:
		authed_user_nick = authed_user.nickname()
	## Graph visualisation.
	file_name_without_extension = file

	# Replaced by a spinning canvas on the clientside
	# if not ds.check_exists(GRAPH_BUCKET + '/' + file_name_without_extension + '.png', None):
	# 	file_name_without_extension = None

	#TODO: Might need to be simplified or moved to a function in fileinfo
	# TODO the folowing should be replaced by a method in the APIDatastore
	lst = ds.list(DATA_BUCKET)
	file_info = None
	for temp_file in lst:
		temp_file.filename = temp_file.filename.rpartition('/')[2]
		if temp_file.filename == file:
			file_info = temp_file;
	return render(request, 'file_preview.html', {'current_file' : file_info, 'authed_user_nick': authed_user_nick, 'file_name_without_extension' : file_name_without_extension})

###########################################################################
## \brief 	view for graph preview pagelet
## \param 	request - Django variable defining the request that triggered
##			the generation of this page
## \note 	only the main panel is generated here, see app(request) for
##			fetching the page's skeleton
## \return 	the main panel pagelet
## \todo	use datastore/permissions API for file list lookup
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
def file_page(request, file=None):
	lst = ds.list('/fc-raw-data')
	file_info = None
	for temp_file in lst:
		temp_file.filename = temp_file.filename.rpartition('/')[2]
		if temp_file.filename == file:
			file_info = temp_file;
	return render(request, 'file_preview.html', {'current_file' : file_info, 'authed_user_nick': authed_user_nick, 'file_name_without_extension' : file_name_without_extension})

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
	return fetch_file(GRAPH_BUCKET + '/' + graph + ".png", 'image/png')

###########################################################################
## \brief Is called when a file is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param dataset - the name of the dataset to be downloaded
## \return the file requested
###########################################################################
def get_dataset(request, dataset):
	return fetch_file(DATA_BUCKET + '/' + dataset, 'application/vnd.isac.fcs')

###########################################################################
## \brief Is called when a info is requested
## \param request - Django variable defining the request that triggered the generation of this page
## \param dataset - the name of the file to be downloaded
## \return the file requested
###########################################################################
def get_info(request, infofile):
	return fetch_file(INFO_BUCKET + '/' + infofile, 'text/html')

###########################################################################
## \brief Return a response containing the file
## \param path - path to the file to be sent to the client
## \param type - type of the file sent (it's mime type)
## \return an HttpResponse ccontaining the file to be sent
###########################################################################
def fetch_file(path, type):
	# TODO: Need protection against hack such as ../
	buffer = ds.open(path)
	if buffer:
		file = buffer.read()
		# TODO: Maybe transform the httpresponse to streaminghttpresponse in case the graph is really large and to improve efficiency
		response = HttpResponse(file, content_type=type)
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
	return render(request, 'settings.html')

###########################################################################
## \brief Is called when a rectangular gating is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param params - Paramesters of this gating, string of the form: topLeftx,topLefty,bottomRightx,bottomRighty,newFilename
## \return a JSON object in a httpresponse, containing the status of the gating, a short message and the link to the newly created graph
###########################################################################
def rect_gating(request, params):
	paramList = params.split(',')

	if len(paramList) == 5 :
		#Reoder the point to take the topLeft and bottomRight points of the square 
		if paramList[0] > paramList[2]:
			tempcoor = paramList[0]
			paramList[0] = paramList[2]
			paramList[2] = tempcoor
		if paramList[1] > paramList[3]:
			tempcoor = paramList[1]
			paramList[1] = paramList[3]
			paramList[3] = tempcoor

		gatingRequest =" ".join(paramList[0:4])        

		newName = paramList[-1] + "-rectGate";
		queue.gate_rectangle(paramList[-1], gatingRequest, newName);

		status = "success"
		message = "the rectangular gating was performed correctly"
		url = reverse('get_graph', args=[newName])
	else:
		status = "fail"
		message = "notcorrect " + params + " length:" + str(len(paramList)) + " is not equal to 4"
		url = None
		 
	return HttpResponse(generate_gating_answer(status, message, url), content_type="application/json")

###########################################################################
## \brief Is called when a polygonal gating is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param params - Paramesters of this gating, string of the form: x1,y1,x2,y2,...xn,yn,newFilename
## \return a JSON object in a httpresponse, containing the status of the gating, a short message and the link to the newly created graph
###########################################################################
def poly_gating(request, params):
	paramList = params.split(',')

	if len(paramList)%2 == 1 :
		gatingRequest = " ".join(paramList[0:-1])        

		newName = paramList[-1] + "-polyGate";
		queue.gate_polygon(paramList[-1], gatingRequest, newName);

		status = "success"
		message = "the polygonal gating was performed correctly"
		url = reverse('get_graph', args=[newName]) 
	else:
		status = "fail"
		message = "notcorrect " + params + " #pointCoordinates:" + str(len(paramList))-1 + " is not pair"
		url = None
		 
	return HttpResponse(generate_gating_answer(status, message, url), content_type="application/json")

###########################################################################
## \brief Is called when an oval gating is requested.
## \param request - Django variable defining the request that triggered the generation of this page
## \param params - Paramesters of this gating, string of the form: meanx,meany,point1x,point1y,point2x,point2y,newFilename
## \return a JSON object in a httpresponse, containing the status of the gating, a short message and the link to the newly created graph
###########################################################################
def oval_gating(request, params):
	paramList = params.split(',')

	if len(paramList) == 7 :
		gatingRequest = " ".join(paramList[0:-1])        

		newName = paramList[-1] + "-ovalGate";
		queue.gate_circle(paramList[-1], gatingRequest, newName);

		status = "success"
		message = "the oval gating was performed correctly"
		url = reverse('get_graph', args=[newName])
	else:
		status = "fail"
		message = "notcorrect " + params + " #pointCoordinates:" + str(len(paramList)) + " is not even"
		url = None

	return HttpResponse(generate_gating_answer(status, message, url), content_type="application/json")

###########################################################################
## \brief create a JSON string containing the status, message and graph's url of a gating response
## \param status - Status of the gating (success or fail)
## \param message - Message containing more information about the gating's status
## \param url - Url to the new gated dataset's graph
## \return a JSON object containing the status of the gating, a short message and the link to the newly created graph
###########################################################################
def generate_gating_answer(status, message, url):
	return simplejson.dumps({"status" : status, "message" : message, "imgUrl" : url});
