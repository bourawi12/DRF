from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class EmployeeProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    bio = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)

class Skill(models.Model):
    profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    prificiency = models.CharField(max_length=50)
    
class Education(models.Model):
    profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    start_year = models.DateField()
    end_year = models.DateField(null=True, blank=True)

class Certification(models.Model):
    profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issued_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
class Project(models.Model):
    profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies_used = models.CharField(max_length=200)
    project_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)