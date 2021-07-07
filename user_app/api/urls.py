from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user_app.api import views


urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    # path('logout/', views.logout, name='logout'),
    path('register/', views.registration_view, name='register'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('logout2/', views.logout2, name='logout2'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
