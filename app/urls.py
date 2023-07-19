from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home,name = "home"),
    path('',views.base,name ="base"),
    path('register_finder/',views.register_finder,name="register_finder"),
    path('register_company/',views.register_company,name="register_company"),
    path('login/',views.login_user,name="login"),
    path('profileA/', views.profileA, name='profileA'),
    path('profileE/', views.profileA, name='profileE'),
    path('profileJF/', views.profileA, name='profileJF'),
    path('settings/',views.settings, name='settings'),
    path('logout', views.logout_user, name='logout'), 
    path('post/', views.post, name='post'),
    path('publish/', views.publish, name='publish'),
    path('apply/', views.apply, name='apply'),
    path('about/',views.about,name='about'),
]
