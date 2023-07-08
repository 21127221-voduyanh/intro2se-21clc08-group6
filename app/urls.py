from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home,name = "home"),
    path('',views.base,name ="base"),
    path('register_finder/',views.register_finder,name="register_finder"),
    path('register_company/',views.register_company,name="register_company"),
    path('login/',views.login_user,name="login"),
    path('profile/', views.profile, name='profile'),
]
