import django_filters
from .models import Ranobe, Tags, Genres, Author, Publisher


class RanobeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags', conjoined=True, queryset=Tags.objects.all())
    genres = django_filters.ModelMultipleChoiceFilter(field_name='genres', conjoined=True,
                                                      queryset=Genres.objects.all())
    adult = django_filters.BooleanFilter(field_name='adult_status')
    author = django_filters.ModelChoiceFilter(field_name='author', queryset=Author.objects.all())
    publisher = django_filters.ModelChoiceFilter(field_name='publisher', queryset=Publisher.objects.all())
    class Meta:
        model = Ranobe
        fields = ['tags', 'genres', 'adult', 'author', 'publisher']
