from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name = "home"),
    # path('',views.base,name ="base"),
    path('register_finder/',views.register_finder,name="register_finder"),
    path('register_company/',views.register_company,name="register_company"),
    path('login/',views.login_user,name="login"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('settings/',views.settings, name='settings'),
    path('logout', views.logout_user, name='logout'), 
    path('post/<int:post_id>/', views.post, name='post'),
    path('publish/', views.publish, name='publish'),
    path('apply/<int:post_id>/', views.apply, name='apply'),
    path('about/',views.about,name='about'),
    path('search/',views.search,name='search'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('history/',views.history, name='history'),
    path('post/edit/<int:pk>/', views.edit_post, name='edit_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
