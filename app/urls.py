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
    path('profileE/', views.profileE, name='profileE'),
    path('profileJF/', views.profileJF, name='profileJF'),
    path('settings/',views.settings, name='settings'),
    path('logout', views.logout_user, name='logout'),
    path('edit', views.edit, name='edit'),
]
