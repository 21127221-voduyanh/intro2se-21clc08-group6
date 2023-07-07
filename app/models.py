from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Job_finder(models.Model):
    id = 0
    id = 0
    full_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    gender=models.CharField(max_length=10)
    address=models.TextField()
    city=models.TextField()
    date_of_birth=models.TextField()
    introduction=models.TextField()
    

class Employer(models.Model):
    id = 1
    id = 1
    company_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    address=models.TextField()
    city=models.TextField()
    introduction=models.TextField()