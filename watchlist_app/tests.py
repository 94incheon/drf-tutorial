from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

from watchlist_app import models
from watchlist_app.api import serializers


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='qwer1234!')
        self.data = {
            'username': 'example',
            'password': 'qwer1234!'
        }
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.refresh_token = response.data.get('refresh')
        self.access_token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.stream = models.StreamPlatform.objects.create(name='Netflix',
                                                           about='#1 Platform',
                                                           website='https://www.netflix.com')

    def test_streamplatform_create(self):
        data = {
            'name': 'Netflix',
            'about': '#1 Streaming Platform',
            'website': 'https://netflix.com'
        }
        response = self.client.post(reverse('streamplatform-list'), data)  # router의 basename-list
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
