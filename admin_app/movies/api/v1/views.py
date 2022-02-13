from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from .mixins import MovieApiMixin


class MoviesListApi(MovieApiMixin, BaseListView):
    """Класс, который реализует получение информации по КП,
       при GET запросе на movies
   """
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формируем контекст для ответа вьюхи."""
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by,
        )

        context = {
            'results': list(queryset),
            'count': paginator.count,
            'next': page.next_page_number() if page.has_next() else None,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'total_pages': paginator.num_pages,
        }

        return context


class MoviesDetailAPI(MovieApiMixin, BaseDetailView):
    """Класс, который реализует получение информации по одному КП."""

    def get_context_data(self, **kwargs):
        """Достаём из контекста, который сформировал
           BaseDetailView, нужный нам объект и возвращаем новый контекст.
        """
        context = super().get_context_data()['object']

        return context
