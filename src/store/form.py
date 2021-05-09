from django import forms
from .models import Product

class search_bar(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']
        widgets = {
        'name': forms.TextInput(attrs={'class': 'search-bar', 'placeholder': 'Search'})
        }