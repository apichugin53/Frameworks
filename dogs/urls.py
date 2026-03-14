from django.urls.conf import path
from django.views.decorators.cache import cache_page, never_cache

from dogs import views
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('dogs/', cache_page(10)(views.DogsListView.as_view()), name='dogs_list'),
    path('dogs/create/', views.DogCreateView.as_view(), name='dog_create'),
    path('dogs/<int:pk>/', cache_page(10)(views.DogDetailsView.as_view()), name='dog_details'),
    path('dogs/<int:pk>/comment/', views.DogCommentAddView.as_view(), name='dog_add_comment'),
    path('dogs/comment/<int:pk>/update/', views.DogCommentUpdateView.as_view(), name='dog_update_comment'),
    path('dogs/<int:pk>/delete/', views.DogDeleteView.as_view(), name='dog_delete'),
    path('dogs/<int:pk>/update/', never_cache(views.DogUpdateView.as_view()), name='dog_update'),
    path('breeds/', cache_page(600)(views.BreedsListView.as_view()), name='breeds_list'),
    path('breeds/<int:pk>/', cache_page(600)(views.BreedDetailsView.as_view()), name='breed_details'),
]
