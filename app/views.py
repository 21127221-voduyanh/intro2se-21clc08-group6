from django.shortcuts import render
from django.http import HttpResponse
from app.models import CustomUser, Employer, Job_finder
from django.contrib import messages
from django.contrib.auth import authenticate
# Create your views here.

def home(request):
    return render(request,'app/home.html')

def base(request):
    return render(request,'app/base.html')

def register_finder(request):
    if( request.method == "POST" ):
        f_name = request.POST.get("fname")
        gender = request.POST.get("gender")
        name = request.POST.get("uname")
        password = request.POST.get("pass")
        r_password = request.POST.get("rpass")
        date = request.POST.get("date")
        addr = request.POST.get("addr")
        city = request.POST.get("city")
        intro = request.POST.get("intro")

        if(password != r_password):
            messages.error(request, 'Passwords must match')
        else:
            user = CustomUser.objects.create_user(username=name, password=password)
            user.is_job_finder = True
            user.address = addr
            user.full_name = f_name
            user.city = city
            user.date_of_birth = date
            user.gender = gender
            user.introduction = intro
            user.save()
            return redirect('login')
        
    return render(request,'app/register_finder.html')

def register_company(request):
    if( request.method == "POST" ):
        c_name = request.POST.get("cname")
        name = request.POST.get("uname")
        password = request.POST.get("pass")
        r_password = request.POST.get("rpass")
        addr = request.POST.get("addr")
        city = request.POST.get("city")
        intro = request.POST.get("intro")

        if(password != r_password):
            messages.error(request, 'Passwords must match')
        else:
            user = CustomUser.objects.create_user(username=name, password=password)
            user.is_employer = True
            user.address = addr
            user.company_name = c_name
            user.city = city
            user.introduction = intro
            user.save()
            return redirect('login')
        
    return render(request,'app/register_company.html')

def login(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        password = request.POST.get("pass")
    
        user = authenticate(request, username=uname, password=password)

        if user is not None:
            messages.error(request, "Success")
            
    return render(request,'app/login.html')
