from django.urls.conf import path

from dogs import views
from dogs.apps import DogsConfig


app_name = DogsConfig.name


urlpatterns = [
    path('', views.index, name='home'),
    path('dogs/', views.dogs_list, name='dogs_list'),
    path('dogs/create/', views.dog_create, name='dog_create'),
    path('dogs/<int:pk_id>/', views.dog_details, name='dog_details'),
    path('dogs/<int:pk_id>/update/', views.dog_update, name='dog_update'),
    path('dogs/<int:pk_id>/delete/', views.dog_delete, name='dog_delete'),
    path('breeds/', views.breeds_list, name='breeds_list'),
    path('breeds/<int:pk_id>/', views.breed_details, name='breed_details'),
]