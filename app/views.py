from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'app/home.html')

def base(request):
    return render(request,'app/base.html')

def register_finder(request):
    return render(request,'app/register_finder.html')