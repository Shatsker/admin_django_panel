from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db.models import Q

from movies.models import Filmwork, PersonFilmWork


class MovieApiMixin:
    """Миксин для API"""
    model = Filmwork
    http_method_names = ('get', )

    def get_queryset(self):
        """Делаем запрос на полную информацию по КП.
           Актеров, сценаристов и режиссёров собираем по отдельным спискам.
        """
        full_info_queryset_of_filmworks = self.model.objects.all().values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
        ).annotate(
            genres=ArrayAgg(
                'genres__name',
                distinct=True,
            ),
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(persons__personfilmwork__role=PersonFilmWork.RoleTypes.ACTOR),
                distinct=True,
            ),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(persons__personfilmwork__role=PersonFilmWork.RoleTypes.DIRECTOR),
                distinct=True,
            ),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(persons__personfilmwork__role=PersonFilmWork.RoleTypes.WRITER),
                distinct=True,
            ),
        )

        return full_info_queryset_of_filmworks

    def render_to_response(self, context, **response_kwargs):
        """Возвращаем контекст в json'е."""
        return JsonResponse(context)
