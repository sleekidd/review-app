from django.shortcuts import render, HttpResponse
from .models import Movie

# Create your views here.


def home(request):
    return render(request, 'movieapp/index.html')


def about(request):
    return render(request, 'movieapp/about.html', {'title': 'About'})
