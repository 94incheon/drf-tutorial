from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

'''
실제 DB를 사용하지 않으므로 안심할것
자동으로 Test DB가 생성되고 다시 삭제된다.
`python manage.py test <app_name>`
'''


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password': 'qwer1234!',
            'password2': 'qwer1234!',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # 값이 서로 틀리면 Error!


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='qwer1234!')
        self.data = {
            'username': 'example',
            'password': 'qwer1234!'
        }
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.refresh_token = response.data.get('refresh')
        self.access_token = response.data.get('access')

    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='bearer ' + self.refresh_token)
        response = self.client.post(reverse('logout2'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
