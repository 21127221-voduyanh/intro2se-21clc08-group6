from django.db import models
from django.contrib.auth.models import User
DATE_INPUT_FORMATS = ['%m-%d-%Y']

# Create your models here.
class Job_finder(models.Model):
    id = 0
    full_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    gender=models.CharField(max_length=100)
    address=models.TextField()
    city=models.TextField()
    date_of_birth=models.DateField()
    introduction=models.TextField()
    

class Employer(models.Model):
    id = 1
    company_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    address=models.TextField()
    city=models.TextField()
    introduction=models.TextField()