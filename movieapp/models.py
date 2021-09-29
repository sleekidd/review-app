import string
import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

# Create your models here.

def rand_slug():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Cast(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='cast_pics')

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='director_pics')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Movie(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # image = models.ImageField(
    #     upload_to='upload/', blank=True, null=True, default='static/img/aquaman.jpg')
    image = models.ImageField(default='default.jpg', upload_to='movie_pics')
    poster = models.ImageField(default='default.jpg', upload_to='poster_pics')
    trailer = models.CharField(max_length=15, null=True)
    cast = models.ManyToManyField(Cast)
    category = models.ManyToManyField(Category)
    director = models.ManyToManyField(Director)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'slug': self.slug})

    @property
    def number_of_comments(self):
        return Review.objects.filter(movie=self).count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
        super(Movie, self).save(*args, **kwargs)


class Review(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='review')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_date']

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return 'Review {} by {}'.format(self.review, self.author, self.id)
