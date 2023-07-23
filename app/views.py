from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app.models import Employer, Job_finder, User, Post, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from app.form import EUpdateForm, JFUpdateForm, PostForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    user =request.user
    employer = None

    # Check if the user is an employer and has an employer profile
    if user.is_authenticated and hasattr(user, 'employer'):
        employer = user.employer

    # Get all posts and exclude hidden posts of other users
    if employer:
        posts = Post.objects.filter(Q(is_hidden=False) | Q(employer=employer)).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_hidden=False).order_by('-created_at')

    p = Paginator(posts, 1)
    page = request.GET.get('page')
    posts = p.get_page(page)
    nums = 'n' * posts.paginator.num_pages
    context = {'posts': posts, 'nums': nums, 'user': request.user}
    return render(request,'app/home.html',context)

def base(request):
    user = request.user
    context = {'user': user}
    return render(request,'app/base.html',context)

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

        check_user =  authenticate(request, username=name, password=password)
        if check == False:
            messages.error(request, "Please accept the terms")
        elif(password != r_password):
            messages.error(request, 'Passwords must match')
        elif check_user is not None:
            messages.error(request, 'Username existed, please choose another username')
        else:
            user = User.objects.create_user(username=name, password=password)
            user.is_job_finder = True
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
        
    return render(request,'app/user/register_finder.html')

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

        check_user =  authenticate(request, username=name, password=password)

        if check == False:
            messages.error(request, "Please accept the terms")
        elif(password != r_password):
            messages.error(request, 'Passwords must match')
        elif check_user is not None:
            messages.error(request, 'Username existed, please choose another username')
        else:
            user = User.objects.create_user(username=name, password=password)
            user.is_employer = True
            user.save()
            em = Employer.objects.create(user=user)
            em.address = addr
            em.company_name = c_name
            em.city = city
            em.introduction = intro
            em.save()
            return redirect('login')
        
    return render(request,'app/user/register_company.html')

def login_user(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        password = request.POST.get("pass")
    
        user = authenticate(request, username=uname, password=password)

        if user is not None and user.is_job_finder:
            auth_login(request, user)
            return redirect('home')
        elif user is not None and user.is_employer:
            auth_login(request, user)
            return redirect('home')
        elif user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Username doesn\'t exist or Password is incorrect')
            
    return render(request,'app/user/login.html')

@login_required(login_url="/login/")
def profile(request,username):
    user2 = User.objects.get(username=username) 
    if user2.is_authenticated:
        if user2.is_job_finder:
            if request.method == 'POST':
                u_form = JFUpdateForm(request.POST, instance=user2.job_finder)
                if u_form.is_valid():
                    u_form.save()
                    messages.success(request, 'Your account has been updated!')
                    return redirect('profile')

            else:
                u_form = JFUpdateForm(instance=user2.job_finder)

            jf = Job_finder.objects.get(user=user2)
            context = {'user2':user2,'jf': jf, 'u_form': u_form}
            return render(request, 'app/user/profileJF.html', context)
        
        elif user2.is_employer:
            if request.method == 'POST':
                u_form = EUpdateForm(request.POST, instance=user2.employer)
                if u_form.is_valid():
                    u_form.save()
                    messages.success(request, 'Your account has been updated!')
                    return redirect('profile')

            else:
                u_form = EUpdateForm(instance=user2.employer)

            em = Employer.objects.get(user=user2)
            context = {'user2':user2,'em': em, 'u_form': u_form}
            return render(request, 'app/user/profileE.html', context)
        
    return redirect('home')

def logout_user(request):
    logout(request)

    return redirect('home')

def settings(request):
    if request.method == 'POST':
        action = request.POST.get('Security')
        
        if action == 'ChangePassword' :
            old_password = request.POST.get('old_pass')
            new_password = request.POST.get('pass')
            confirm_password = request.POST.get('rpass')
           
            u = request.user
    
            user_change = authenticate(request, username=u.username, password=old_password)

            if user_change is not None:
                if new_password == confirm_password:
                    user_change.set_password(new_password)
                    user_change.save()
                    auth_login(request, user_change)
                    logout(request)
                    return redirect('login')
                else :
                    messages.error(request, "Passwords must match", extra_tags='changepassword')
            elif user_change is None:
                messages.error(request, "Invalid password", extra_tags='changepassword')

        elif action == 'DeleteAccount': 
            delete_password = request.POST.get('dpass')
            u = request.user

            user_delete = authenticate(request,username=u.username,password = delete_password)

            if user_delete is not None:
                user_delete.delete()
                logout(request)
                return redirect('home')
            elif user_delete is None :
                messages.error(request, "Invalid password", extra_tags='deleteaccount')

    return render(request,'app/settings.html')
    
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    user = request.user
    is_owner = False
    if user == post.employer.user:
        is_owner = True

    if request.method == 'POST':
        action = request.POST.get('action') 
        if action == 'like':
            if user in post.likes.all():
                post.likes.remove(user)
                post.is_liked = False
            else:
                post.likes.add(user)
                post.dislikes.remove(user)
                post.is_like = True

        elif action == 'dislike':
            if user in post.dislikes.all():
                post.dislikes.remove(user)
                post.is_disliked = False
            else:
                post.dislikes.add(user)
                post.likes.remove(user)
                post.is_dislike = True
        # Process comment submission
        elif action == 'comment':
            content = request.POST.get('comment_content')
            comment = Comment(user=request.user, post=post, content=content)
            comment.save()
        # Handle hiding and unhiding the post
        elif is_owner and action == 'hide':
            post.is_hidden = True
            post.save()

        elif is_owner and action == 'unhide':
            post.is_hidden = False
            post.save()
        #Handle delete post
        elif is_owner and action=='delete':
            post.delete()
            return redirect('home')

    return render(request, 'app/post/post.html', {'post': post, 'comments': comments, 'is_owner': is_owner})

def publish(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)   
        if form.is_valid():
            form.instance.employer = request.user.employer
            form.instance.introduction=request.user.employer.introduction
            form.instance.city=request.user.employer.city
            form.instance.company_name=request.user.employer.company_name
            form.save()
            messages.error(request, "Post created successfully")
        else:
            messages.error(request, "Please complete all information")

    return render(request, 'app/post/publish.html', {'form':form})

def apply(request):
    return render(request,'app/post/apply.html')

def about(request):
    return render(request,'app/about.html')

def search(request):
    return render(request,'app/search.html')

