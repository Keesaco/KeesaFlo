from django.http import HttpResponse
from django.shortcuts import render
from django import forms
import forms
from django.core.files.uploadhandler import FileUploadHandler
import upload_handling


def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def faq(request):
	return render(request, 'faq.html')

def app(request):
	return render(request, 'app.html')

def settings(request):
	return render(request, 'settings.html')

# Testing code for data upload
def upload(request):
    request.upload_handlers = [upload_handling.fcsUploadHandler()]
    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        #print request.FILES
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse('File uploaded to %s' % request.FILES['file'].path)
        else:
            return render(request, 'upload.html', {'form': form})
    else:
        form = forms.UploadFile()
        return render(request, 'upload.html', {'form': form})