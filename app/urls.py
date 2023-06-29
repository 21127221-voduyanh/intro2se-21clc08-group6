from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home,name = "home"),
    path('',views.base,name ="base"),
    path('register_finder/',views.register_finder,name="register_finder"),
]
