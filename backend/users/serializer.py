from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import Profile, BookReadingStatus, ReadHistory, RanobeLikes
from ranobe.models import Ranobe


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        Profile.objects.create(
            user=user
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(source='profile.profile_img')
    birth_date = serializers.DateField(source='profile.birth_date')

    class Meta:
        model = User
        fields = ('username', 'email', 'img', 'birth_date')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_img', 'birth_date')


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RanobeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranobe
        fields = ('id',)


class UserSerializerRelation(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializerRelation(serializers.Serializer):
    user = UserSerializer(many=False, required=True)

    class Meta:
        model = Profile
        fields = ('bookmarked',)


class BookmarkSerializer(serializers.Serializer):
    id = serializers.CharField(source='user.id')
    bookmarks = serializers.PrimaryKeyRelatedField(source='bookmarked', read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ['id', 'bookmarks']


class BookStatusSerializer(serializers.Serializer):
    id = serializers.CharField(source='user.id')
    reading = serializers.PrimaryKeyRelatedField(source='reading_books', read_only=True, many=True)
    planned = serializers.PrimaryKeyRelatedField(source='planned_books', read_only=True, many=True)
    read = serializers.PrimaryKeyRelatedField(source='read_books', read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ['id', 'reading', 'planned', 'read']


class BookReadingStatusSerializer(serializers.Serializer):
    id = serializers.CharField(source='user.id')
    read_status = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ['id', 'read_status']


class UpdateBookReadingStatusSerializer(serializers.Serializer):
    class Meta:
        model = BookReadingStatus

    def update(self, instance, validated_data):
        instance.profile_id = validated_data.get('user', instance.user)
        instance.ranobe_id = validated_data.get('ranobe_id', instance.ranobe_id)
        instance.choices = validated_data.get('choice', instance.choice)
        return instance


class UpdateBookmarkSerializer(serializers.Serializer):
    class Meta:
        model = Profile

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.bookmarked.add(validated_data.get('ranobe_id', instance.ranobe_id))
        return instance


class ProfileBookmarkSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = "bookmarked"


class BookreadingStatusProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = "__all__"


class AnotherProfileSerializer(serializers.ModelSerializer):
    born = serializers.ReadOnlyField(source='profile.birth_date', read_only=True)
    img = serializers.ImageField(source='profile.profile_img', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'born', 'img']


class ReadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadHistory
        fields = '__all__'


class UserLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RanobeLikes
        fields = "__all__"