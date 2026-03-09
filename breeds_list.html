from django.forms import ModelForm
from django.forms.fields import FileField
from django.forms.widgets import FileInput, TextInput, Textarea, Select
from django.utils.safestring import SafeString

from dogs.models import Dog


class DogForm(ModelForm):
    photo = FileField(label='Фото', required=False, widget=FileInput(attrs={'class': 'form-control'}))

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Dog
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'breed': Select(attrs={'class': 'form-select'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }