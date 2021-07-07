from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from watchlist_app import models


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
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

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
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title='Example Movie!',
                                                         storyline='Example Movie',
                                                         active=True)

    def test_watchlist_create(self):
        data = {
            'platform': self.stream,
            'title': 'Example Movie',
            'storyline': 'Example Story',
            'active': True
        }
        response = self.client.post(reverse('watchlist-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('watchlist-detail', args=(self.watchlist.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, 'Example Movie!')
        self.assertEqual(User.objects.count(), 1)


class ReviewTestCase(APITestCase):

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
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title='Example Movie!',
                                                         storyline='Example Movie',
                                                         active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream,
                                                          title='Example Movie2!',
                                                          storyline='Example Movie2',
                                                          active=True)
        self.review = models.Review.objects.create(review_user=self.user,
                                                   watchlist=self.watchlist2,
                                                   rating=5,
                                                   description='This is Good Movie forever!',
                                                   active=True)

    def test_review_create(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'Great Movie!',
            'watchlist': self.watchlist,
            'active': True
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        self.assertEqual(models.Review.objects.get(watchlist=self.watchlist).rating, 5)

        response = self.client.post(reverse('review-create', args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'Great Movie!',
            'watchlist': self.watchlist,
            'active': True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            'review_user': self.user,
            'rating': 4,
            'description': 'Great Movie! - updated',
            'watchlist': self.watchlist,
            'active': False
        }

        response = self.client.put(reverse('review-detail', args=(self.review.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get(reverse('user-review-detail'), params={'username': self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
