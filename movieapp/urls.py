from django.urls import path
from .views import (
    # MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    SearchResultsView,
    rate
)
from . import views

urlpatterns = [
    path('', views.home, name='movie-home'),
    # path('movies/', views.movies, name='movie-all'),
    path('movies/', views.movies, name='movie-all'),
    path('movie/<slug:slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movie/new/', MovieCreateView.as_view(), name='movie-create'),
    path('movie/<int:pk>/update/', MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie-delete'),
    path('about/', views.about, name='movie-about'),
    path('rate/', rate, name='rate-view'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
