from django.urls import path

from users.apps import UsersConfig
from users.views import UserListView, UserDetailsView, UserDogsView, UserEditView, UserActiveStatusView, UserCommentsView, UserRoleView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailsView.as_view(), name='user_details'),
    path('<int:pk>/comments/', UserCommentsView.as_view(), name='user_comments'),
    path('<int:pk>/dogs/', UserDogsView.as_view(), name='user_dogs'),
    path('<int:pk>/edit/', UserEditView.as_view(), name='user_edit'),
    path('<int:pk>/status/', UserActiveStatusView.as_view(), name='user_status'),
    path('<int:pk>/role/', UserRoleView.as_view(), name='user_role'),
    path('profile/', UserDetailsView.as_view(), name='profile'),
    path('profile/comments/', UserCommentsView.as_view(), name='profile_comments'),
    path('profile/dogs/', UserDogsView.as_view(), name='profile_dogs'),
    path('profile/edit/', UserEditView.as_view(), name='profile_edit'),
]
