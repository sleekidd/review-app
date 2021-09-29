import json
from typing import cast
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Movie, Cast, Review
from django.utils import timezone
from .forms import ReviewForm
from django.http import JsonResponse
from django.db.models import Avg, Func, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'


def home(request):
    context = {
        'movies': Movie.objects.filter(
            release_date__lte=timezone.now()).order_by('-release_date')[:6].annotate(avg_score=Round(Avg('review__rating'))).annotate(review_count=Count('title'))
    }
    return render(request, 'movieapp/index.html', context)


def movies(request):
    movie_list = Movie.objects.filter(
                release_date__lte=timezone.now()).order_by('-release_date').annotate(avg_score=Round(Avg('review__rating'))
        ).annotate(review_count=Count('title'))

    page = request.GET.get('page', 1)

    paginator = Paginator(movie_list, 3)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    return render(request, 'movieapp/movies.html', { 'movies': movies })


def rate(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        review = request.POST.get('review')
        movie = Review.objects.get(id=movie_id)
        rating = request.POST.get('rating')
        user = request.user
        Review(user=user, movie=movie, review=review, rating=rating)

        return redirect('movie_detail', id=movie_id)

        # context = {
        #     'u_form': u_form,
        #     'p_form': p_form
        # }
        # return render(request, 'users/profile.html', context)


# class MovieListView(ListView):
#     model = Movie
#     template_name = 'movieapp/movies.html'  # <app>/<model>_<viewtype>/html
#     context_object_name = 'movies'
#     ordering = ['-release_date']
#     paginate_by = 6

    # def movies(request):
    #     context = {
    #         'rating': Movie.objects.filter(
    #             release_date__lte=timezone.now()).order_by('-release_date')[:6].annotate(avg_score=Round(Avg('review__score')))
    #     }
    #     return render(request, 'movieapp/movies.html', context)

    # def get_queryset(self): # new
    #     movies = Movie.objects.filter(
    #             release_date__lte=timezone.now()).order_by('-release_date')[:6].annotate(avg_score=Round(Avg('review__score'))
    #     )
    #     return movies


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

        movie_rating = Movie.objects.annotate(avg_score=Round(Avg('review__rating'))).annotate(review_count=Count('title'))
        data['movie_ratings'] = movie_rating

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Review(review=request.POST.get(
            'review'), rating=request.POST.get('rating'), author=self.request.user, movie=self.get_object())

        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class MovieCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Movie
    fields = ['title', 'content', 'image', 'poster', 'cast', 'slug', 'trailer', 'category', 'director', 'release_date']

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
    fields = ['title', 'content', 'image', 'poster', 'cast', 'slug', 'trailer', 'category', 'director', 'release_date']

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

class SearchResultsView(ListView):
    model = Movie
    template_name = 'movieapp/search_results.html'
    # queryset = Movie.objects.filter(title__icontains='the') # new
    
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Movie.objects.filter(
            Q(title__icontains=query)
        ).annotate(avg_score=Round(Avg('review__rating'))).annotate(review_count=Count('title'))
        return object_list


def about(request):
    return render(request, 'movieapp/about.html', {'title': 'About'})
