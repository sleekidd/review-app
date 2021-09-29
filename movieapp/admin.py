from django.contrib import admin
from .models import Director, Movie, Cast, Category, Review, Director

# Register your models here.
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Category)
admin.site.register(Director)
# admin.site.register(Comment)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'movie',
                    'created_date', 'approved_comment')
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('author', 'review')
    actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)
