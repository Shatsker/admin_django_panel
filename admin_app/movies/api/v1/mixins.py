from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db.models import Q

from movies.models import Filmwork, PersonFilmWork


class MovieApiMixin:
    """Миксин для API"""
    model = Filmwork
    http_method_names = ('get', )
    type_of_person_for_getting_data = {
        PersonFilmWork.RoleTypes.ACTOR,
        PersonFilmWork.RoleTypes.WRITER,
        PersonFilmWork.RoleTypes.DIRECTOR,
    }

    def get_queryset(self):
        """Делаем запрос на полную информацию по КП.
           Актеров, сценаристов и режиссёров собираем по отдельным спискам.
        """

        persons_from_filmwork = {}
        for person_type in self.type_of_person_for_getting_data:
            persons_from_filmwork[person_type] = self.get_filmwork_person(person_type)

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
            **persons_from_filmwork
        )

        return full_info_queryset_of_filmworks

    @staticmethod
    def get_filmwork_person(role_name):
        return ArrayAgg(
            'persons__full_name',
            filter=Q(persons__personfilmwork__role=role_name),
            distinct=True,
        )

    def render_to_response(self, context, **response_kwargs):
        """Возвращаем контекст в json'е."""
        return JsonResponse(context)
