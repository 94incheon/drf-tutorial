from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.WatchListAPI.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchDetailAPI.as_view(), name='movie-detail'),

    path('stream/', views.StreamPlatformAPI.as_view(), name='stream-list'),
    path('stream/<int:pk>/', views.StreamPlatformDetailAPI.as_view(), name='stream-detail'),
]
