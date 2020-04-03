from rest_framework import serializers
from .models import Ranobe, Author, Chapters, Tags, Genres


class RanobeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranobe
        fields = ['id', 'name', 'description', 'publisher_id', 'author_id', 'image', 'adult_status', 'alternate_name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author']


class DetailRanobeSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(source='get_author_name', read_only=True)
    publisher_name = serializers.SerializerMethodField(source='get_publisher_name', read_only=True)
    genres_name = serializers.SerializerMethodField(source='get_genres_name', read_only=True)
    tags_name = serializers.SerializerMethodField(source='get_tags_name', read_only=True)

    class Meta:
        model = Ranobe
        fields = '__all__'

    def get_author_name(self, obj):
        try:
            return obj.author.author
        except AttributeError:
            return 'Нет автора'

    def get_publisher_name(self, obj):
        try:
            return obj.publisher.publisher
        except AttributeError:
            return 'Нет издателя'

    def get_genres_name(self, obj):
        try:
            return [x.genre for x in obj.genres.all()]
        except (AttributeError, IndexError):
            return []

    def get_tags_name(self, obj):
        try:
            return [x.tag for x in obj.tags.all()]
        except (AttributeError, IndexError):
            return []


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapters
        fields = ("id", 'chapter_name')

class DetailChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapters
        fields = "__all__"

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class GenresSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = "__all__"
