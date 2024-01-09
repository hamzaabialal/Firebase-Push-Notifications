from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

class SignUpModel(AbstractUser):
    full_name = models.CharField(max_length=100)    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100) 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class CustomUser(models.Model):
    user = models.ForeignKey(SignUpModel, on_delete=models.CASCADE, related_name="custom_user")
    token = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)

class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    recipient_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    status = models.CharField(max_length=100, choices=(('unread', 'unread'), ('read', 'read')), default='unread')

    def __str__(self):
        return self.title


class Profile(models.Model):
    email = models.ForeignKey(SignUpModel, on_delete=models.CASCADE, related_name="profile")
    token = models.CharField(default='',max_length=1000)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.email)
    
    def save(self, *args, **kwargs):
        self.token = str(uuid.uuid4())
        super(Profile, self).save(*args, **kwargs)