from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _

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

    error_css_class = 'danger'


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

    error_css_class = 'danger'

    class Meta:
        model = User
        fields = ('username', 'email',)
