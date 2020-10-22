from django.urls import path
from .views import (
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView
)
from . import views

urlpatterns = [
    # path('', views.home, name='movie-home'),
    path('', MovieListView.as_view(), name='movie-home'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movie/new/', MovieCreateView.as_view(), name='movie-create'),
    path('movie/<int:pk>/update/', MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie-delete'),
    path('about/', views.about, name='movie-about'),
]
