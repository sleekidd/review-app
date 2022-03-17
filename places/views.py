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
from .models import Movie, Cast, Place, Review
from django.utils import timezone
from .forms import ReviewForm
from django.http import JsonResponse
from django.db.models import Avg, Func, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    context = {
        'places': Place.objects.filter(
            release_date__lte=timezone.now()).order_by('-release_date')[:6]
    }
    return render(request, 'movieapp/index.html', context)