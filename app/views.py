###########################################################################
## \file app/views.py
## \brief Generates the pages to be sent to the client using templates files
## \author mrudelle@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
## \author jmccrea@keesaco.com
###########################################################################

from django.http import HttpResponse
from django.http import HttpResponseNotFound  
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import forms
from django.core.files.uploadhandler import FileUploadHandler
import upload_handling
import API.APIDatastore as ds
import API.PALUsers as auth

DATA_BUCKET = '/fc-raw-data'
GRAPH_BUCKET = '/fc-vis-data'

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
            return redirect('app')
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
    for temp_file in lst: 
        temp_file.filename = temp_file.filename.rpartition('/')[2]
    return render(request, 'file_list.html', {'files' : lst})

def file_preview(request, file = None):
    ## Authentication.
    authed_user = auth.get_current_user()
    if authed_user is None:
        authed_user_nick = 'Guest'
    else:
        authed_user_nick = authed_user.nickname()
    ## Graph visualisation.
    file_name_without_extension = file
    if not ds.check_exists(GRAPH_BUCKET + '/' + file_name_without_extension + '.png', None):
        file_name_without_extension = None
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

def get_graph(request, graph):
    return fetch_file(GRAPH_BUCKET + '/' + graph + ".png", 'image/png')

def get_dataset(request, dataset):
    return fetch_file(DATA_BUCKET + '/' + dataset, 'application/vnd.isac.fcs')

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
