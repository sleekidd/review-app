from django.shortcuts import render, HttpResponse
from .models import Movie

# Create your views here.


def home(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request, 'movieapp/index.html', context)


def about(request):
    return render(request, 'movieapp/about.html', {'title': 'About'})
