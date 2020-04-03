import django_filters
from .models import Ranobe, Tags, Genres


class RanobeFilter(django_filters.FilterSet):
    # tags = django_filters.CharFilter(field_name='tags', lookup_expr='tags')
    # genres = django_filters.CharFilter(field_name='genres', lookup_expr='genres')
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags', conjoined=True, queryset=Tags.objects.all())
    genres = django_filters.ModelMultipleChoiceFilter(field_name='genres', conjoined=True, queryset=Genres.objects.all())
    adult = django_filters.BooleanFilter(field_name='adult_status')
    class Meta:
        model = Ranobe
        fields = ['tags', 'genres', 'adult']
        # fields = {"tags": ['exact'],
        #           'genres': ['exact']}
