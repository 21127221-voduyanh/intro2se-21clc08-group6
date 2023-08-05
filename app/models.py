from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import math

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
    pic_url = models.ImageField()
    company_name=models.CharField(default="",max_length=100)
    contact = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.TextField(default="")
    city=models.TextField(default="")
    caption = models.CharField(max_length=255)
    address = models.TextField()
    fields = ( ('Medicine', 'Medicine'),
            ('Law', 'Law'),
            ('Information Technology', 'Information Technology'),
            ('Finance and Banking', 'Finance and Banking'),
            ('Business Management', 'Business Management'),
            ('Education', 'Education'),
            ('Insurance Business', 'Insurance Business'),
            ('Real Estate', 'Real Estate'),
            ('Tourism', 'Tourism'),
            ('Electronics/Electricity', 'Electronics/Electricity'),
            ('Architecture', 'Architecture'),
            ('Hotel and Restaurant', 'Hotel and Restaurant'),
            ('Construction/Building', 'Construction/Building'),
            ('Finacial Investment', 'Finacial Investment'),
        )
    field = models.CharField(choices=fields)
    job = models.CharField()
    description = models.TextField()
    hour = models.CharField(max_length=255)
    salaries = ( ('Below 100$','Below 100$'),
               ('100$ - 200$','100$ - 200$'),
               ('200$ - 400$','200$ - 400$'),
               ('400$ - 600$','400$ - 600$'),
               ('600$ - 800$','600$ - 800$'),
               ('800$ - 1000$','800$ - 1000$'),
               ('Above 1000$','Above 1000$'),
               )
    salary = models.CharField(choices=salaries)

    deny = models.TextField()
    approve = models.TextField()

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Hide function uses here
    is_hidden = models.BooleanField(default=False)
    # Additional fields
    likes = models.ManyToManyField(User, related_name='liked_posts')
    dislikes = models.ManyToManyField(User, related_name='disliked_posts')
    
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    # Time posted function
    def __str__(self):
        return self.caption


    def time_posted(self):
        now = timezone.now()
        
        diff = now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_comments', blank=True)

class CV(models.Model):
    finder = models.ForeignKey(Job_finder, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    address = models.TextField()
    date_of_birth = models.TextField()
    introduction = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    interest = models.TextField()
    languages = models.TextField()
    skill = models.TextField()
    mail = models.EmailField()
    phone = models.CharField()

class Dashboard(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    applied_time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DENIED', 'Denied'),
        ('HIDE', 'Hide'),
        ('HIGHTLIGHT', 'Hightlight')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

class ApplicationHistory(models.Model):
    job_finder = models.ForeignKey(Job_finder, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    job_applied = models.CharField(max_length=200)
    applied_time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DENIED', 'Denied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    content = models.TextField(default="")
    is_user = models.BooleanField(default=False)
    is_post = models.BooleanField(default=False)
    reported_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reported',null=True, blank=True)
    reported_post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True, blank=True,)