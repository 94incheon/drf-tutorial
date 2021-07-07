from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('', views.WatchListAPI.as_view(), name='watchlist-list'),
    path('<int:pk>/', views.WatchDetailAPI.as_view(), name='watchlist-detail'),

    path('', include(router.urls)),

    path('<int:pk>/reviews/create/', views.ReviewCreateAPI.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewListAPI.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailAPI.as_view(), name='review-detail'),

    path('user-reviews/', views.UserReview.as_view(), name='user-review-detail'),
]
