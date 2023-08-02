from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app.models import Employer, Job_finder, User, Post, Comment, CV
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from app.form import EUpdateForm, JFUpdateForm, PostForm, CVForm
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from collections import Counter

# Create your views here.

def base():
    post_list = Post.objects.all()
    cf = Counter([obj.field for obj in post_list]).most_common(3)
    slr = Counter([obj.salary for obj in post_list]).most_common(7)
    ct = Counter([obj.city for obj in post_list]).most_common(6)
    return cf,slr,ct

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

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    nums = 'n' * posts.paginator.num_pages
    cf,slr,ct = base()
    context = {'posts': posts, 'nums': nums, 'user': request.user, 'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/home.html',context)

def register_finder(request):
    cf,slr,ct = base()
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
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/user/register_finder.html',context)

def register_company(request):
    cf,slr,ct = base()
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
    context = {'cf': cf, 'slr': slr, 'ct':ct}   
    return render(request,'app/user/register_company.html',context)

def login_user(request):
    cf,slr,ct = base()
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
    context = {'cf': cf, 'slr': slr, 'ct':ct}      
    return render(request,'app/user/login.html',context)

@login_required(login_url="/login/")
def profile(request,username):
    cf,slr,ct = base()
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
            context = {'user2':user2,'jf': jf, 'u_form': u_form, 'cf': cf, 'slr': slr, 'ct':ct}
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
            context = {'user2':user2,'em': em, 'u_form': u_form, 'cf': cf, 'slr': slr, 'ct':ct}
            return render(request, 'app/user/profileE.html', context)
        
    return redirect('home')

def logout_user(request):
    logout(request)

    return redirect('home')

def settings(request):
    cf,slr,ct = base()
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
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/settings.html',context)
    
def post(request, post_id):
    cf,slr,ct = base()
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    user = request.user
    is_owner = user == post.employer.user if user.is_authenticated else False
    liked_comments = Comment.objects.filter(post=post, likes=user)
    disliked_comments = Comment.objects.filter(post=post, dislikes=user)
    context = {
        'post': post,
        'comments': comments,
        'is_owner': is_owner,
        'liked_comments': liked_comments,
        'disliked_comments': disliked_comments,
        'cf': cf, 'slr': slr, 'ct':ct
    }   
    post.is_liked = user in post.likes.all()
    post.is_disliked = user in post.dislikes.all()
    

    if request.method == 'POST':
        action = request.POST.get('action') 
        #like/dislike post
        if action == 'like':
            if user in post.likes.all():
                post.likes.remove(user)
                post.is_liked = False
            else:
                post.likes.add(user)
                post.dislikes.remove(user)
                post.is_liked = True
                post.is_disliked = False
            return redirect('post', post_id=post_id)

        elif action == 'dislike':
            if user in post.dislikes.all():
                post.dislikes.remove(user)
                post.is_disliked = False
            else:
                post.dislikes.add(user)
                post.likes.remove(user)
                post.is_disliked = True
                post.is_liked= False
            return redirect('post', post_id=post_id)
        #like/dislike comments

        elif action =='like_comment':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            if user in comment.likes.all():
                comment.likes.remove(user)
            else:
                comment.likes.add(user)
                comment.dislikes.remove(user)

            # Update the liked_comments and disliked_comments after processing the like action
            liked_comments = Comment.objects.filter(post=post, likes=user)
            disliked_comments = Comment.objects.filter(post=post, dislikes=user)

            return redirect('post', post_id=post_id)

        elif action == 'dislike_comment':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            if user in comment.dislikes.all():
                comment.dislikes.remove(user)
            else:
                comment.dislikes.add(user)
                comment.likes.remove(user)

            # Update the liked_comments and disliked_comments after processing the dislike action
            liked_comments = Comment.objects.filter(post=post, likes=user)
            disliked_comments = Comment.objects.filter(post=post, dislikes=user)

            return redirect('post', post_id=post_id)
        # Process comment submission
        elif action == 'comment':
            content = request.POST.get('comment_content')
            comment = Comment(user=request.user, post=post, content=content)
            comment.save()
            return redirect('post', post_id=post_id)
        # Handle hiding and unhiding the post
        elif is_owner and action == 'hide':
            post.is_hidden = True
            post.save()
            return redirect('post', post_id=post_id)

        elif is_owner and action == 'unhide':
            post.is_hidden = False
            post.save()
            return redirect('post', post_id=post_id)
        #Handle delete post
        elif is_owner and action=='delete':
            post.delete()
            return redirect('home')

    return render(request, 'app/post/post.html', context)

def publish(request):
    cf,slr,ct = base()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)   
        if form.is_valid():
            form.instance.employer = request.user.employer
            form.instance.introduction=request.user.employer.introduction
            form.instance.city=request.user.employer.city
            form.instance.company_name=request.user.employer.company_name
            form.save()
            messages.error(request, "Post created successfully")
        else:
            messages.error(request, "Please complete all information")
    context = {'form':form, 'cf': cf, 'slr': slr, 'ct':ct}
    return render(request, 'app/post/publish.html', context)

def about(request):
    cf,slr,ct = base()
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/about.html',context)

def search(request):
    cf,slr,ct = base()
    if request.GET.get('apply') == 'applied':
        messages.error(request,'Sort applied')
    searched = request.GET.get('searched', "")
    check = False
    sort = request.GET.get('sort',"")
    category = request.GET.get('category',"")
    searched_cate = ''


    if any(category == x[0] for x in cf) and sort == 'postdate':
        check = True
        searched_cate = 'Field: ' + category
        posts = Post.objects.filter(field=category).order_by('-created_at')
        count = Post.objects.filter(field=category).order_by('-created_at').count()
    elif any(category == x[0] for x in cf):
        searched_cate = 'Field: ' + category
        posts = Post.objects.filter(field=category)
        count = Post.objects.filter(field=category).count()
    elif any(category == x[0] for x in slr) and sort == 'postdate':
        check = True
        searched_cate = 'Salary: ' + category
        posts = Post.objects.filter(salary=category).order_by('-created_at')
        count = Post.objects.filter(salary=category).order_by('-created_at').count()
    elif any(category == x[0] for x in slr):
        searched_cate = 'Salary: ' + category
        posts = Post.objects.filter(salary=category)
        count = Post.objects.filter(salary=category).count()
    elif any(category == x[0] for x in ct) and sort == 'postdate':
        check = True
        searched_cate = 'City: ' + category
        posts = Post.objects.filter(city=category).order_by('-created_at')
        count = Post.objects.filter(city=category).order_by('-created_at').count()
    elif any(category == x[0] for x in ct):
        searched_cate = 'City: ' + category
        posts = Post.objects.filter(city=category)
        count = Post.objects.filter(city=category).count()
    elif sort == 'postdate':
        check = True
        posts = Post.objects.filter(caption__icontains=searched).order_by('-created_at')
        count = Post.objects.filter(caption__icontains=searched).order_by('-created_at').count
    else:
        posts = Post.objects.filter(caption__icontains=searched)
        count = Post.objects.filter(caption__icontains=searched).count
    p = Paginator(posts, 10)
    page = request.GET.get('page',1)
    try:
        posts = p.page(page)
    except EmptyPage:
        posts = p.page(p.num_pages)
    except:
        posts = p.page(1)
    nums = 'n' * posts.paginator.num_pages
    context = {'searched':searched, 'posts':posts,'nums':nums, 'count':count,'check': check, 'sort': sort, 'category': category,
               'searched_cate': searched_cate, 'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/search.html',context)

def apply(request):
    cf,slr,ct = base()
    form = CVForm()
    if request.method == 'POST':
        form = CVForm(request.POST)   
        if form.is_valid():
            form.instance.finder = request.user.job_finder
            form.instance.full_name = request.user.job_finder.full_name
            form.instance.gender = request.user.job_finder.gender
            form.instance.address = request.user.job_finder.address
            form.instance.date_of_birth = request.user.job_finder.date_of_birth
            form.save()
            messages.error(request, "CV created successfully")
        else:
            messages.error(request, "Please complete all information")
    context = {
        'job_finder' : request.user.job_finder,
        'form' : form,
        'cf': cf, 'slr': slr, 'ct':ct
    }
    return render(request, 'app/post/apply.html', context)

def dashboard(request):
    cf,slr,ct = base()
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/post/dashboard.html',context)

def history(request):
    cf,slr,ct = base()
    context = {'cf': cf, 'slr': slr, 'ct':ct}
    return render(request,'app/post/history.html',context)