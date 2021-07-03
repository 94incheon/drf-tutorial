from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.MovieListAPI.as_view(), name='movie-list'),
    path('<int:pk>/', views.MovieDetailAPI.as_view(), name='movie-detail'),
]
