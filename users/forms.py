from django import forms
from django.contrib.auth import get_user_model
from django.db.models import F
from django.forms import TextInput
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput

from core.widgets import ImageFileInput

User = get_user_model()


class UserEditForm(ModelForm):
    error_css_class = 'error-wrapper'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'avatar': ImageFileInput(attrs={'class': 'form-control'}),
        }


class UserRoleForm(ModelForm):
    role = forms.CharField(widget=HiddenInput())

    class Meta:
        model = User
        fields = ('role',)


class UserActiveStatusForm(ModelForm):
    class Meta:
        model = User
        fields = ()

    def save(self, **kwargs):
        self.instance.is_active = ~F('is_active')
        return super().save(**kwargs)
