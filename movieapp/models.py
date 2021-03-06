from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Cast(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='cast_pics')

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
    cast = models.ManyToManyField(Cast)
    category = models.ManyToManyField(Category)
    release_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'pk': self.pk})

    @property
    def number_of_comments(self):
        return Review.objects.filter(movie=self).count()


class Review(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='review')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_date']

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return 'Review {} by {}'.format(self.content, self.author)
