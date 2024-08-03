from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields here
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # sign_in_time = models.DateTimeField()
    # sign_out_time = models.DateTimeField(blank=True, null=True)
    sign_in_time = models.TimeField(auto_now_add=True)
    sign_out_time = models.TimeField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Token(models.Model):
    date = models.DateField(auto_now_add=True)
    remote_token = models.CharField(max_length=50)
    onsite_token = models.CharField(max_length=50)
