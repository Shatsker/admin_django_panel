from django.urls import path

from . import views


urlpatterns = (
    path('movies/', views.MoviesListApi.as_view(), name='movies'),
    path('movies/<uuid:pk>/', views.MoviesDetailAPI.as_view(), name='detail_movie'),
)
