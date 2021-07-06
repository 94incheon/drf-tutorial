from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from watchlist_app.models import Review, WatchList, StreamPlatform
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.serializers import (ReviewSerializer, WatchListSerializer,
                                           StreamPlatformSerializer)


'''
Class Base View
'''


class ReviewCreateAPI(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    # 특정 영화에 대한 리뷰를 생성하기 위함
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        review_user = self.request.user

        watchlist = WatchList.objects.get(pk=pk)

        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie!')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewListAPI(generics.ListAPIView):
    # queryset = Review.objects.all() # 현재 영화에 대한 리뷰를 받고싶은데, 모든리뷰를 리턴중
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


# class ReviewDetailAPI(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewAPI(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return StreamPlatform.objects.prefetch_related('watchlist', 'watchlist__reviews').all()


# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, pk):
#         platform = get_object_or_404(StreamPlatform, pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.prefetch_related('watchlist').all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})  # HyperLinkedField, HyperLinkModelSerializer
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StreamPlatformDetailAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        platform = get_object_or_404(StreamPlatform, pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.select_related('platform').prefetch_related('reviews').all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WatchDetailAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        movie = get_object_or_404(WatchList, pk=pk)
        serializer = WatchListSerializer(movie, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        movie = get_object_or_404(WatchList, pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)  # 인자중요
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        movie = get_object_or_404(WatchList, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
Function Base View
'''
# @api_view(['GET', 'POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)

#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         serializer = MovieSerializer(movie, data=request.data)  # 인자중요
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
