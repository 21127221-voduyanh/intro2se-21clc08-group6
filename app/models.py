from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_job_finder = models.BooleanField(default=False)

class Job_finder(models.Model):
    full_name=models.CharField(max_length=100)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE, primary_key=True)
    gender=models.CharField(max_length=10)
    address=models.TextField()
    city=models.TextField()
    date_of_birth=models.DateTimeField()
    introduction=models.TextField()
    

class Employer(models.Model):
    company_name=models.CharField(max_length=100)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE, primary_key=True)
    address=models.TextField()
    city=models.TextField()
    introduction=models.TextField()