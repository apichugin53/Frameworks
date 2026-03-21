from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordResetForm, \
    PasswordChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_variables

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
        }),
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
        }),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
        }),
    )
    error_css_class = 'error-wrapper'

    class Meta:
        model = User
        fields = ('username', 'email',)

    def save(self, commit=True, **kwargs):
        user = super().save(commit)
        context = {
            "user": user.username,
            **kwargs,
        }
        message = render_to_string('security/registration_email.html', context)
        user.email_user(
            subject=f'Registration',
            message='Registration complete.',
            html_message=message,
            fail_silently=False,
        )
        return user


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'email',
        }),
    )
    error_css_class = 'error-wrapper'


class PasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': 'form-control',
        }),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': 'form-control',
        }),
    )


class PwdChangeForm(PasswordForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "autofocus": True,
            'class': 'form-control',
        }),
    )
    error_css_class = 'error-wrapper'
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _(
            "Your old password was entered incorrectly. Please enter it again."
        ),
    }
    field_order = ["old_password", "new_password1", "new_password2"]

    @sensitive_variables("old_password")
    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password
