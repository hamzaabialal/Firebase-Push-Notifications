from django.shortcuts import render
from django.http import JsonResponse
from.models import CustomUser, Notification
from .serializers import CustomUserSerializer, NotificationSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from django.db.models.signals import post_save
import json
from django.http import HttpResponse
# Create your views here.


class NotificationView(ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CustomUserView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


def send_notification(registration_ids, message_title):
    fcm_api = "AAAAFbxdlzk:APA91bFD7evskcY-D1-HtxK6YGWA_FV2Dm9hFH7lmAq1fqtcNnaNA03rn8WJzypyoz0CpFpQXYlNQWPMRuwtiQGqKqbhlPiSmHQ6Lj0rft0f7Sr0gcdmcZgqXlcS9UGMJ3iZwUxD6Cr6"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api}

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            # "body": message_desc,
            "title": message_title,
            "image": "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",

        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.json())


def index(request):
    return render(request, 'home.html')


@receiver(post_save, sender=Notification)
def send_push_notification(sender, instance, created, **kwargs):
    if created:  # only send notification for newly created PushNotification
        # Fetch the FCM tokens and create a registration list
        fcm_tokens = CustomUser.objects.values_list('token', flat=True)

        # Here, you might have a condition to filter tokens for specific users or criteria
        # For example: fcm_tokens = FCMToken.objects.filter(user=some_user).values_list('token', flat=True)
        # Construct registration list using fetched tokens
        registration = list(fcm_tokens)

        # Example static registration for illustration purposes
        registration += [
            'eVwLxhH1iHfVNG45Xoc4aO:APA91bGOv0D1nvCvsW5gQyojdtvL2sMQt5PFjIqrDh3SFwFI3PIlXpfD_8mcHlNChPeFFtUr9PVKPcNdUhbIlnVim8E7sGMbGn8fcomivONUhOomJFbfzEC4rHTLMW8FDpVqBKOATPdX']

        push_notification_title = instance.title
        push_notification_body = instance.body
        push_notification_time_stamp = instance.time_stamp

        send_notification_to_user(registration, push_notification_title)


def send(request):
    return HttpResponse("sent")


def send_notification_to_user(registration, push_notification_title):
    send_notification(registration, push_notification_title)


def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyBhYZw16H_y8kF1EaFDAa9bz3sJYBH-3Co",' \
           '        authDomain: "freelance-2dbde.firebaseapp.com",' \
           '        projectId: "freelance-2dbde",' \
           '        storageBucket: "freelance-2dbde.appspot.com",' \
           '        messagingSenderId: "93354563385",' \
           '        appId: "1:93354563385:web:9613d67324542e49a47ae8",' \
           '        measurementId: "G-93QKQXN3YM"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")


@csrf_exempt
def send_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token_data = data.get('token')  # Access token from the POST request
        # Perform actions with the token data (e.g., save it, process it)
        # For now, just echo the token as a JSON response
        return JsonResponse({'received_token': token_data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)