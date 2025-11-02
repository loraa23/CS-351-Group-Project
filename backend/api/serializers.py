from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Event, Schedule


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
        
# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ['title', 'start_time', 'end_time', 'campus', 'days', 'building', 'room', 'author']
#         extra_kwargs = {"author": {"read_only": True}}

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['title', 'file', 'uploaded_at', 'author']
        extra_kwargs = {"author": {"read_only": True}}