from rest_framework import serializers
from .models import Review
from main.models import Restaurants

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    restaurant = serializers.StringRelatedField(read_only=True)  # Display the restaurant name
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurants.objects.all(),  # Correct queryset for validation
        source='restaurant',  # Map to the `restaurant` field in the model
        write_only=True
    )

    def validate_restaurant_id(self, value):
        print(f"Validating restaurant_id: {value}")
        return value

    class Meta:
        model = Review
        fields = ['id', 'user', 'restaurant', 'restaurant_id', 'rating', 'description', 'created_at']
