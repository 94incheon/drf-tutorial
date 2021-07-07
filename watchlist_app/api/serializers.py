from rest_framework import serializers

from watchlist_app.models import Review, WatchList, StreamPlatform


# class WatchListSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = WatchList
#         fields = '__all__'


# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):  # url name 중요
#     watchlist = WatchListSerializer(many=True, read_only=True)

#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ['watchlist']
        # fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)  # 역참조
    platform = serializers.CharField(source='platform.name')  # source

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):  # 1
    watchlist = WatchListSerializer(many=True, read_only=True)  # N (related_name)
    # watchlist = serializers.StringRelatedField(many=True) # __str__ 반환
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # pk값 반환
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')  # view > context

    class Meta:
        model = StreamPlatform
        fields = '__all__'


# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField(min_length=10)
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     # Object-Level Validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 'Name and Description should be different')
#         else:
#             return data

#     # Field-Level Validation
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Name is too short!!')
#         else:
#             return value
