from django import forms
from .models import Review
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    # I added this function so that the test.py could run correctly
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return rating

    class Meta:
        model = Review
        fields = ['rating', 'description']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'text-white font-bold bg-[#2F2821]'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'text-white bg-[#2F2821] font-bold',
                'style': 'max-width: 200px;' 
            }),
        }
