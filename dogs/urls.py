from django.urls.conf import path

from dogs import views
from dogs.apps import DogsConfig


app_name = DogsConfig.name


urlpatterns = [
    path('', views.index, name='home'),
    path('dogs/', views.dogs_list, name='dogs_list'),
    path('dogs/<int:id>/', views.dog_details, name='dog_details'),
    path('breeds/', views.breeds_list, name='breeds_list'),
    path('breeds/<int:id>/', views.breed_details, name='breed_details'),
]