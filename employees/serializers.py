from rest_framework import serializers
from .models import Employee, Review

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['employee', 'content', 'created_at']

class EmployeeSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True) 

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'department', 'contact_info', 'is_active', 'reviews']
