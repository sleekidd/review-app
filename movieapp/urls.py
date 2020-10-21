from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='movie-home'),
    path('about/', views.about, name='movie-about'),
]
