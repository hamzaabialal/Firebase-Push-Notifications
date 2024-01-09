"""
URL configuration for FirebaseNotification project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import NotificationView, CustomUserView, send_mail_to_all, send_notification, index, showFirebaseJS, send_token, send, NotificationVIewSet ,UserSignUpView, UserLoginInView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('signup', UserSignUpView, basename="signup")
router.register('login', UserLoginInView, basename="login")



urlpatterns = [
    path('', include(router.urls)),

    path('notifcication/', NotificationView.as_view()),
    path('customuser/', CustomUserView.as_view()),
    path('send-notification/', send_notification),
    path('index/', index),
    path('firebase-messaging-sw.js', showFirebaseJS),
    path('send-token/', send_token),
    path('send/', send),
    path('notificationview/', NotificationVIewSet.as_view()),
    path('send_mail/', send_mail_to_all)


]
