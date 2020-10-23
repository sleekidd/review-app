from django.shortcuts import render, HttpResponse, get_object_or_404, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Movie, Cast, Review
from django.utils import timezone
from .forms import ReviewForm

# Create your views here.


def home(request):
    context = {
        'movies': Movie.objects.filter(
            release_date__lte=timezone.now()).order_by('release_date')[:3]
    }
    return render(request, 'movieapp/index.html', context)


class MovieListView(ListView):
    model = Movie
    template_name = 'movieapp/movies.html'  # <app>/<model>_<viewtype>/html
    context_object_name = 'movies'
    ordering = ['-release_date']
    paginate_by = 2


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movieapp/movie_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Review.objects.filter(
            movie=self.get_object()).order_by('-created_date')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = ReviewForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Review(content=request.POST.get(
            'content'), author=self.request.user, movie=self.get_object())

        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class MovieCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Movie
    fields = ['title', 'content', 'image', 'cast', 'category', 'release_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # movie = self.get_object()
        # if self.request.user == movie.author:
        if self.request.user.is_superuser:
            return True
        return False


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    fields = ['title', 'content', 'image', 'cast', 'category', 'release_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        movie = self.get_object()
        # if self.request.user == movie.author:
        if self.request.user.is_superuser:
            return True
        return False


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    success_url = '/'

    def test_func(self):
        movie = self.get_object()
        # if self.request.user == movie.author:
        if self.request.user.is_superuser:
            return True
        return False


def about(request):
    return render(request, 'movieapp/about.html', {'title': 'About'})
