from django.contrib import admin
from .models import Movie, Cast, Category

# Register your models here.
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Category)
