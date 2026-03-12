from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('<int:pk>/', views.ProfileView.as_view(), name='user_details'),
    path('<int:pk>/update', views.ProfileUpdate.as_view(), name='user_update'),
]