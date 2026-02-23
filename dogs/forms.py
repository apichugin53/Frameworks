from django import forms
from .models import Dog

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'age', 'color', 'weight', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }
