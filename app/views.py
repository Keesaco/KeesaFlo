from django.http import HttpResponse
from django.http import HttpResponseNotFound  
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import forms
from django.core.files.uploadhandler import FileUploadHandler
import upload_handling
import API.APIDatastore as ds;

GRAPH_BUCKET = '/fc-vis-data'
#GRAPH_BUCKET = '/fc-raw-data'

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def faq(request):
	return render(request, 'faq.html')

def app(request):
    request.upload_handlers = [upload_handling.fcsUploadHandler()]
    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            return redirect('app')
        else:
            return render(request, 'app.html', {'form': form})
    else:
        form = forms.UploadFile()
        return render(request, 'app.html', {'form': form})

def file_list(request):
    lst = ds.list('/fc-raw-data')
    for temp_file in lst: 
        temp_file.filename = temp_file.filename.rpartition('/')[2]
    return render(request, 'file_list.html', {'files' : lst})

def file_preview(request, file=None):
    lst = ds.list('/fc-raw-data')
    file_info = None
    file_name_without_extension = None
    for temp_file in lst: 
        temp_file.filename = temp_file.filename.rpartition('/')[2]
        if temp_file.filename == file:
            file_info = temp_file;
            file_name_without_extension = "".join(file.split(".")[0:-1])
            #TODO: Might need to be siplified or moved to a fonction in fileinfo
    return render(request, 'file_preview.html', {'current_file' : file_info, 'file_name_without_extension' : file_name_without_extension})

def settings(request):
	return render(request, 'settings.html')

def pagenav(request):
	return render(request, 'pagenav.html')

def toolselect(request):
	return render(request, 'toolselect.html')

def get_graph(request, graph):
    # Need protection against hack such as ../
    buffer = ds.open(GRAPH_BUCKET + '/' + graph)
    if buffer:
        file = buffer.read()
        response = HttpResponse(file, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="' + graph + '"'
        return response
    else:
        return HttpResponseNotFound('<h1>' + graph + ' doesn\'t has any visualisation data</h1>')