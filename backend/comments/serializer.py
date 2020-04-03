from rest_framework import serializers
from .models import Comments


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.username')
    user_id = serializers.ReadOnlyField(source='author.id')
    user_img = serializers.ImageField(source='author.profile.profile_img')

    class Meta:
        model = Comments
        fields = [
            'id',
            'ranobe',
            'user',
            'user_id',
            'user_img',
            'created_on',
            'text'
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'id',
            'ranobe',
            'author_id',
            'text'
        ]

    def create(self, validated_data):
        validated_data['author_id'] = self.context['request'].user.id
        return super(CommentCreateSerializer, self).create(validated_data)


class CommentUpdateDestroySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comments
        fields = [
            'id',
            'text',
            'user'
        ]


class ShortCommentSerializer(serializers.ModelSerializer):
    author_id = serializers.RelatedField(read_only=True, source='profile.id')
    class Meta:
        model = Comments
        fields = [
            'id',
            'text',
            'author_id'
        ]
