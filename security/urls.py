from django.contrib.auth.views import LogoutView
from django.urls import path

from security.apps import SecurityConfig
from security.views import SignInView, SignUpView

app_name = SecurityConfig.name

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
