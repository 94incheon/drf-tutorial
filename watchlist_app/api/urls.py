from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('', views.WatchListAPI.as_view(), name='watchlist-list'),
    path('<int:pk>/', views.WatchDetailAPI.as_view(), name='watchlist-detail'),

    path('', include(router.urls)),

    # path('stream/', views.StreamPlatformAPI.as_view(), name='streamplatform-list'),
    # path('stream/<int:pk>/', views.StreamPlatformDetailAPI.as_view(), name='streamplatform-detail'),  # name - HyperLinkModelSerializer 중요

    # path('review/', views.ReviewListAPI.as_view(), name='review-list'),
    # path('review/<int:pk>/', views.ReviewDetailAPI.as_view(), name='review-detail'),

    path('<int:pk>/review-create/', views.ReviewCreateAPI.as_view(), name='streamplatform-create'),  # 특정영화에 대한 리뷰생성
    path('<int:pk>/reviews/', views.ReviewListAPI.as_view(), name='streamplatform-detail'),  # 영화에대한 모든리뷰
    path('review/<int:pk>/', views.ReviewDetailAPI.as_view(), name='review-detail'),

    # path('review/<str:username>/', views.UserReview.as_view(), name='user-review-detail'),
    path('reviews/', views.UserReview.as_view(), name='user-review-detail'),
]
