from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of the ID
    restaurant = serializers.StringRelatedField()  # Display the restaurant name instead of the ID

    class Meta:
        model = Review
        fields = ['id', 'user', 'restaurant', 'rating', 'description', 'created_at']
