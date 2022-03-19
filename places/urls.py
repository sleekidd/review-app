from django.urls import path
from .views import (
    # MovieListView,
    PlaceDetailView
)

from . import views

urlpatterns = [
    path('places/', views.places, name='place-all'),
    path('place/<slug:slug>/', PlaceDetailView.as_view(), name='place-detail'),
]