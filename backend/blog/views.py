from rest_framework import permissions, generics, mixins, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializer import BlogSerializer
from .models import Blog


class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [permissions.BasePermission]


class DetailBlogView(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.BasePermission]
    queryset = Blog.objects.all()

    def get(self, request, *args, **kwargs):
        post = self.queryset.get(id=kwargs['post_id'])
        resp = self.serializer_class(post).data
        return Response(resp, status=status.HTTP_200_OK)
