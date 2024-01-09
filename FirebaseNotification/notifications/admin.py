from django.contrib import admin
from .models import Notification, Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'is_verified', 'created_at', 'updated_at')
