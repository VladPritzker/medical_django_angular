# medical_app/serializers.py

from rest_framework import serializers
from .models import CustomUser, HealthHistory, Appointment

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'is_active', 'is_staff', 'is_admin']

class HealthHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthHistory
        fields = ['id', 'condition', 'treatment', 'date']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'appointment_date', 'notes']
