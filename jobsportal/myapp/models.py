from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Application(models.Model):
    seeker = models.ForeignKey(User,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seeker.username} applied for {self.job.title}"
    
class SeekerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/',null=True,blank=True)
    skills = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.user.username

