from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from .model_mixins import TimeStampedMixin, UUIDMixin


class Genre(TimeStampedMixin, UUIDMixin):
    """Модель жанров."""

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        indexes = (
            models.Index(fields=('name', ), name='genre_name_idx'),
        )

    def __str__(self):
        return self.name


class Person(TimeStampedMixin, UUIDMixin):
    """Модель для людей в фильмах."""

    class GenderType(models.TextChoices):
        """Для выбора гендера у персоны."""

        MALE = 'male', _('male')
        FEMALE = 'female', _('female')
        OTHER = 'other', _('other')

    full_name = models.TextField(_('full_name'))
    birth_date = models.DateField(null=True, blank=True)
    gender = models.TextField(_('gender'), choices=GenderType.choices, null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        indexes = (
            models.Index(fields=('full_name', ), name='person_full_name_idx'),
        )

    def __str__(self):
        return self.full_name


class Filmwork(TimeStampedMixin, UUIDMixin):
    """Модель кинопроизведений."""

    class FilmworkTypes(models.TextChoices):
        """Типы кинопроизведений."""

        MOVIE = 'MOVIE', _('movie')
        TV_SHOW = 'TV_SHOW', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    creation_date = models.DateField(_('creation_date'))
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(
        _('file_path'),
        blank=True,
        null=True,
        upload_to='movies/',
    )
    rating = models.FloatField(
        _('rating'),
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
    )
    type = models.CharField(
        _('filmwork_type'),
        choices=FilmworkTypes.choices,
        max_length=255,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        indexes = (
            models.Index(fields=('creation_date', ), name='film_work_creation_date_idx'),
        )

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    """Связи жанров и кинопроизведений."""

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = (
            models.Index(fields=('film_work_id', 'genre_id', ), name='film_work_genre_idx'),
        )


class PersonFilmWork(UUIDMixin):
    """Связи людей с кинопроизведениями."""

    class RoleTypes(models.TextChoices):
        """Типы ролей для персон в фильмах/сериалах."""

        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        PRODUCER = 'producer', _('producer')
        EDITOR = 'editor', _('editor')
        WRITER = 'writer', _('writer')

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True, choices=RoleTypes.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = (
            models.Index(fields=('film_work_id', 'person_id', ), name='film_work_person_idx'),
        )
