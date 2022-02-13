from django.contrib import admin

from .models import (
    Genre,
    Person,
    Filmwork,
    GenreFilmWork,
    PersonFilmWork,
)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmWork
    raw_id_fields = ('genre', )


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork
    raw_id_fields = ('person', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = ('full_name', )
    search_fields = ('full_name', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):

    inlines = (PersonFilmworkInline, GenreFilmworkInline)
    list_display = ('title', 'type', 'creation_date', 'rating')
    list_filter = ('type', 'genres__name')
    search_fields = ('title', 'description', 'id')

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.prefetch_related('genres', 'persons')
