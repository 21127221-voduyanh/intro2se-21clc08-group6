from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_job_finder = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

class Job_finder(models.Model):
    full_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    gender=models.CharField(max_length=100)
    address=models.TextField()
    city=models.TextField()
    date_of_birth=models.TextField()
    introduction=models.TextField()

class Employer(models.Model):
    company_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    address=models.TextField()
    city=models.TextField()
    introduction=models.TextField()

class Post(models.Model):
    pic_url = models.URLField()
    caption = models.CharField(max_length=255)
    address = models.TextField()
    job = models.CharField(max_length=255)
    description = models.TextField()
    hour = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Additional fields
    likes = models.ManyToManyField(User, related_name='liked_posts')
    dislikes = models.ManyToManyField(User, related_name='disliked_posts')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)