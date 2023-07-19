from django.contrib import admin
from app.models import User,Employer, Job_finder, Post
# Register your models here.


admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Job_finder)
admin.site.register(Post)