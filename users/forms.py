from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserEditForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')


class UserStatusForm(ModelForm):
    role = forms.CharField(required=False, widget=HiddenInput())
    is_active = forms.CharField(required=False, widget=HiddenInput())

    class Meta:
        model = User
        fields = ('role', 'is_active')

    def save(self, **kwargs):
        is_active = self.data.get('is_active')
        if is_active is not None:
            self.instance.is_active = is_active != 'True'
        return super().save(**kwargs)
