from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _

from users.models import Role

User = get_user_model()


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username or email'),
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'autocapitalize': 'none',
            'autocomplete': 'username email',
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control'
        }),
    )
    error_css_class = 'error-wrapper'


class SignUpForm(UserCreationForm):
    username = UsernameField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'email'
        })
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
    )
    error_css_class = 'error-wrapper'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)


class UserUpdateForm(ModelForm):
    role = forms.CharField(required=False, widget=HiddenInput())
    is_active = forms.CharField(required=False, widget=HiddenInput())

    class Meta:
        model = User
        fields = ('role', 'is_active')

    def save(self, **kwargs):
        role = self.data.get('role')
        is_active = self.data.get('is_active')
        if role:
            self.instance.is_staff = role == Role.ADMIN or role == Role.MODERATOR
            self.instance.is_superuser = role == Role.ADMIN
        if is_active is not None:
            self.instance.is_active = is_active != 'True'
        return super().save(**kwargs)
