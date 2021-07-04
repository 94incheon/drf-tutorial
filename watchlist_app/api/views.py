from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer
from watchlist_app.models import WatchList, StreamPlatform


class StreamPlatformAPI(APIView):

    def get(self, request):
        platforms = StreamPlatform.objects.prefetch_related('watchlist').all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StreamPlatformDetailAPI(APIView):

    def get(self, request, pk):
        platform = get_object_or_404(StreamPlatform, pk=pk)
        serializer = StreamPlatformSerializer(platform)
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

    def get(self, request):
        movies = WatchList.objects.select_related('platform').all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WatchDetailAPI(APIView):

    def get(self, request, pk):
        movie = get_object_or_404(WatchList, pk=pk)
        serializer = WatchListSerializer(movie)
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
