from django.db import models

# Create your models here.
import string
import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Place(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # image = models.ImageField(
    #     upload_to='upload/', blank=True, null=True, default='static/img/aquaman.jpg')
    image = models.ImageField(default='default.jpg', upload_to='place_pics')
    poster = models.ImageField(default='default.jpg', upload_to='poster_pics')
    address = models.TextField()
    website = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    # cast = models.ManyToManyField(Cast)
    category = models.ManyToManyField(Category)
    # director = models.ManyToManyField(Director)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'slug': self.slug})

    # @property
    # def number_of_comments(self):
    #     return Review.objects.filter(movie=self).count()

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(rand_slug() + "-" + self.title)
    #     super(Place, self).save(*args, **kwargs)