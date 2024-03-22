from django import forms
from .models import CustomerReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['rating', 'review']
