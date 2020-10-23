from django.contrib import admin
from .models import Movie, Cast, Category, Review

# Register your models here.
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Category)
# admin.site.register(Comment)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'movie',
                    'created_date', 'approved_comment')
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('author', 'content')
    actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)
