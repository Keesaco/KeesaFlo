from django.http import HttpResponse
from django.shortcuts import render

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