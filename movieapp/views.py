from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Movie

# Create your views here.


def home(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request, 'movieapp/index.html', context)


class MovieListView(ListView):
    model = Movie
    template_name = 'movieapp/index.html'  # <app>/<model>_<viewtype>/html
    context_object_name = 'movies'
    ordering = ['-release_date']


class MovieDetailView(DetailView):
    model = Movie


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    fields = ['title', 'content', 'image', 'cast', 'category', 'release_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    fields = ['title', 'content', 'image', 'cast', 'category', 'release_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.author:
            return True
        return False


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    success_url = '/'

    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.author:
            return True
        return False


def about(request):
    return render(request, 'movieapp/about.html', {'title': 'About'})
