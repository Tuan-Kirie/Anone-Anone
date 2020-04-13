from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Ranobe, Chapters, Tags, Genres
from .serializer import RanobeSerializer, DetailRanobeSerializer, ChapterSerializer, TagsSerializer, GenresSerialzier, \
    DetailChapterSerializer
from rest_framework import permissions, filters, generics
from .filters import RanobeFilter


class StandardPaginationRanobe(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RanobeList(ListAPIView):
    queryset = Ranobe.objects.all()
    serializer_class = RanobeSerializer
    permission_classes = [permissions.BasePermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    pagination_class = StandardPaginationRanobe
    filterset_class = RanobeFilter


class RanobeDetailView(GenericAPIView):
    lookup_field = "id"
    queryset = Ranobe.objects.all()
    serializer_class = DetailRanobeSerializer
    permission_classes = [permissions.BasePermission]

    def get(self, request, pk, format=None):
        """Method to get detail view of ranobe"""
        snippet = self.queryset.get(id=pk)
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)


class StandartChapterPagePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 250


class TagsGenresPagination(PageNumberPagination):
    page_size = 150


class ChapterPageView(ListAPIView):
    serializer_class = ChapterSerializer
    pagination_class = StandartChapterPagePagination
    permission_classes = [permissions.BasePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['chapter_name']

    def get_queryset(self):
        return Chapters.objects.filter(ranobe_id=self.kwargs['pk'])


class DetailChapterPage(generics.RetrieveAPIView):
    serializer_class = DetailChapterSerializer
    # queryset = Chapters.objects.all()
    queryset = Chapters.objects.all()
    permission_classes = [permissions.BasePermission]

    def get_object(self):
        obj = get_object_or_404(Chapters, id=self.kwargs['chapter_id'])
        return obj


class TagsView(ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.BasePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag']
    pagination_class = TagsGenresPagination


class GenresView(ListAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerialzier
    permission_classes = [permissions.BasePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['genre']
    pagination_class = TagsGenresPagination
