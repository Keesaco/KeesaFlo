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

# Testing code for data upload
def upload(request):
    request.upload_handlers = [upload_handling.fcsUploadHandler()]
    if request.method == 'POST':
        form = forms.UploadFile(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse('This file is called %s' % cd['title'])
        else:
            return render(request, 'upload.html', {'form': form})
    else:
        form = forms.UploadFile()
        return render(request, 'upload.html', {'form': form})