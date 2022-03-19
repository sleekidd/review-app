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
from .models import Place
from django.utils import timezone
# from .forms import ReviewForm
from django.http import JsonResponse
from django.db.models import Avg, Func, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def places(request):
    place_list = Place.objects.filter(
                release_date__lte=timezone.now()).order_by('-release_date')

    page = request.GET.get('page', 1)

    paginator = Paginator(place_list, 6)
    try:
        places = paginator.page(page)
    except PageNotAnInteger:
        places = paginator.page(1)
    except EmptyPage:
        places = paginator.page(paginator.num_pages)

    return render(request, 'places/places.html', { 'places': places })

class PlaceDetailView(DetailView):
    model = Place
    template_name = 'places/place_detail.html'

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)

    #     comments_connected = Review.objects.filter(
    #         movie=self.get_object()).order_by('-created_date')
    #     data['comments'] = comments_connected
    #     if self.request.user.is_authenticated:
    #         data['comment_form'] = ReviewForm(instance=self.request.user)

    #     movie_rating = Place.objects.annotate(avg_score=Round(Avg('review__rating'))).annotate(review_count=Count('title'))
    #     data['movie_ratings'] = movie_rating

    #     return data

    # def post(self, request, *args, **kwargs):
    #     new_comment = Review(review=request.POST.get(
    #         'review'), rating=request.POST.get('rating'), author=self.request.user, movie=self.get_object())

    #     new_comment.save()
    #     return self.get(self, request, *args, **kwargs)