from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Employer, Job_finder
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request,'app/home.html')

def base(request):
    return render(request,'app/base.html')

def register_finder(request):
    if( request.method == "POST" ):
        check = request.POST.get("checkbox", False)
        f_name = request.POST.get("fname")
        gender = request.POST.get("gender")
        name = request.POST.get("uname")
        password = request.POST.get("pass")
        r_password = request.POST.get("rpass")
        date = request.POST.get("inputDate")
        addr = request.POST.get("addr")
        city = request.POST.get("city")
        intro = request.POST.get("intro")

        if check == False:
            messages.error(request, "Please accept the terms")
        elif(password != r_password):
            messages.error(request, 'Passwords must match')
        else:
            user = User.objects.create(username=name, password=password)
            user.save()
            jf = Job_finder.objects.create(user=user)
            jf.address = addr
            jf.full_name = f_name
            jf.city = city
            jf.date_of_birth = date
            jf.gender = gender
            jf.introduction = intro
            jf.save()
            return redirect('login')
        
    return render(request,'app/register_finder.html')

def register_company(request):
    if( request.method == "POST" ):
        check = request.POST.get("checkbox", False)
        c_name = request.POST.get("cname")
        name = request.POST.get("uname")
        password = request.POST.get("pass")
        r_password = request.POST.get("rpass")
        addr = request.POST.get("addr")
        city = request.POST.get("city")
        intro = request.POST.get("intro")

        if check == False:
            messages.error(request, "Please accept the terms")
        elif(password != r_password):
            messages.error(request, 'Passwords must match')
        else:
            user = User.objects.create_user(username=name, password=password)
            user.save()
            em = Employer.objects.create()
            em.address = addr
            em.company_name = c_name
            em.city = city
            em.introduction = intro
            em.user = user
            em.save()
            return redirect('login')
        
    return render(request,'app/register_company.html')

def login(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        password = request.POST.get("pass")
    
        user = authenticate(request, username=uname, password=password)

        if user is not None:
            return redirect('home')
            
    return render(request,'app/login.html')


def profile(request):
    user = request.user
    return render(request, 'app/profile.html', {'user': user})