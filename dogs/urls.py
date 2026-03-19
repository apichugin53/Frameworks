from django.urls.conf import path

from dogs import views
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', views.DogsListView.as_view(), name='dogs_list'),
    path('add/', views.DogCreateView.as_view(), name='dog_add'),
    path('<int:pk>/', views.DogDetailsView.as_view(), name='dog_details'),
    path('<int:pk>/delete/', views.DogDeleteView.as_view(), name='dog_delete'),
    path('<int:pk>/update/', views.DogUpdateView.as_view(), name='dog_update'),
    path('<int:pk>/pedigree/', views.DogPedigreeView.as_view(), name='dog_pedigree'),
    path('<int:pk>/comments/', views.DogCommentListView.as_view(), name='dog_comments'),
    path('<int:pk>/comments/add/', views.DogCommentAddView.as_view(), name='dog_comment_add'),
    path('<int:dog_pk>/comments/<int:pk>/delete/', views.DogCommentDeleteView.as_view(), name='dog_comment_delete'),
    path('<int:dog_pk>/comments/<int:pk>/update/', views.DogCommentUpdateView.as_view(), name='dog_comment_update'),
    path('breeds/', views.BreedsListView.as_view(), name='breeds_list'),
    path('breeds/<int:pk>/', views.BreedDetailsView.as_view(), name='breed_details'),
    path('comments/', views.CommentListView.as_view(), name='comments_list'),
    path('comments/<int:pk>/approve/', views.ApproveCommentView.as_view(), name='comment_approve'),
]
