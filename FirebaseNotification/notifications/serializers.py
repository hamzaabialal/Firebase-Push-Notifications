from rest_framework import serializers
from .models import Notification, CustomUser, SignUpModel
from rest_framework.validators import ValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class CustomUserModelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({"error": "Password Does Not Match"})
        return attrs

        
    def create(self, validated_data):
        user =  SignUpModel.objects.create(
            email = validated_data['email'],
            full_name = validated_data['full_name'],
            username= validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
    class Meta:
        model = SignUpModel
        fields = ['id', 'full_name', "email", "password",
                  "confirm_password", "username"]


class LoginInSerializer(serializers.Serializer):

    """User log in serialier """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})        


            

        
