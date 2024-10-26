from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
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
