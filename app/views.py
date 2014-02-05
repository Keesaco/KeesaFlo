from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import forms
from django.core.files.uploadhandler import FileUploadHandler
import upload_handling
import API.APIDatastore as ds;

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def faq(request):
	return render(request, 'faq.html')

def app(request, file=None):
    lst = ds.list('/fc-raw-data')
    file_info = None
    for temp_file in lst: 
        temp_file.filename = temp_file.filename.rpartition('/')[2]
        if temp_file.filename == file :  file_info = temp_file

    request.upload_handlers = [upload_handling.fcsUploadHandler()]
    if request.GET.has_key('xhr'):
        return HttpResponse("<h1>It worked for " + request.GET.__getitem__('xhr') + "</h1>", mimetype="text/html")
    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            return redirect('app')
        else:
            return render(request, 'app.html', {'form': form, 'files' : lst , 'current_file' : file_info})
    else:
        form = forms.UploadFile()
        return render(request, 'app.html', {'form': form, 'files' : lst , 'current_file' : file_info})

def settings(request):
	return render(request, 'settings.html')
