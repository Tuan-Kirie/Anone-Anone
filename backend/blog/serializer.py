from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'name', 'text', 'published_date', 'author', 'author_name']
