import django_filters
from .models import Ranobe, Tags, Genres


class RanobeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags', conjoined=True, queryset=Tags.objects.all())
    genres = django_filters.ModelMultipleChoiceFilter(field_name='genres', conjoined=True,
                                                      queryset=Genres.objects.all())
    adult = django_filters.BooleanFilter(field_name='adult_status')
    likes = django_filters.NumberFilter(field_name='ranobelikes', lookup_expr='gte')

    class Meta:
        model = Ranobe
        fields = ['tags', 'genres', 'adult', 'likes']
