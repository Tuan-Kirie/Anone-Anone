from rest_framework import permissions, generics, mixins, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializer import BlogSerializer
from .models import Blog


class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [permissions.BasePermission]
    #
    # def retrieve(self, request, *args, **kwargs):
    #     return Response(self.serializer_class(Blog.objects.all(), many=True).data, status=status.HTTP_200_OK)
