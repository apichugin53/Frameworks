from django.contrib.auth.views import LogoutView
from django.urls import path

from security.apps import SecurityConfig
from security.views import (SignInView, SignUpView, PwdChangeView, PwdResetView,
                            PwdResetDoneView, PwdResetConfirmView, PwdResetCompleteView)

app_name = SecurityConfig.name

urlpatterns = [
    path('login/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='signout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_change/', PwdChangeView.as_view(), name='password_change'),
    path('password_reset/', PwdResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PwdResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PwdResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PwdResetCompleteView.as_view(), name='password_reset_complete'),
]
