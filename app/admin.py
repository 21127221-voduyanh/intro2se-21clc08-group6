from django.contrib import admin
from app.models import CustomUser, Job_finder, Employer

# Register your models here.

# admin.site.register(CustomUser)
# admin.site.register(Employer)
# admin.site.register(Job_finder)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Job_finder)
class Job_finderAdmin(admin.ModelAdmin):
    pass

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    pass