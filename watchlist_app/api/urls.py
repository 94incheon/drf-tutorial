from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.WatchListAPI.as_view(), name='watchlist-list'),
    path('<int:pk>/', views.WatchDetailAPI.as_view(), name='watchlist-detail'),

    path('stream/', views.StreamPlatformAPI.as_view(), name='streamplatform-list'),
    path('stream/<int:pk>/', views.StreamPlatformDetailAPI.as_view(), name='streamplatform-detail'),  # name - HyperLinkModelSerializer 중요

    path('review/', views.ReviewListAPI.as_view(), name='review-list'),
    path('review/<int:pk>/', views.ReviewDetailAPI.as_view(), name='review-detail'),

    # path('stream/<int:pk>/review/', views.StreamPlatformDetailAPI.as_view(), name='streamplatform-detail'),  # name - HyperLinkModelSerializer 중요
    # path('stream/review/<int:pk>/', views.ReviewDetailAPI.as_view(), name='review-detail'),
]
