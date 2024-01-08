from django.db import models

# Create your models here.
class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    receipent_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=(('unread', 'unread'), ('read', 'read')), default='unread')

    def __str__(self):
        return self.title

