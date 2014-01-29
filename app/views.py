from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import forms
from django.core.files.uploadhandler import FileUploadHandler
import upload_handling
import API.APIDatastore as ds
import API.PALUsers as auth


def login(request):
	link = auth.create_login_url('app/')
	return redirect(link)
	
def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def faq(request):
	return render(request, 'faq.html')

def app(request, file=None):
    lst = ds.list('/fc-raw-data')
    file_info = None
	
	
	## \brief authed bit test for account nicknames
	authed_user = auth.get_current_user()
	if authed_user is None:
		authed_user_nick = "Guest"
	else
		authed_user_nick = authed_user.nickname()
	##############################################
	
    for temp_file in lst: 
        temp_file.filename = temp_file.filename.rpartition('/')[2]
        if temp_file.filename == file :  file_info = temp_file

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

def settings(request):
	return render(request, 'settings.html')
