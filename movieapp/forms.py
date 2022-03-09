from django import forms
from django.core import validators
from django.db.models.expressions import RowRange
from .models import Review
from django.core.validators import MaxValueValidator, MinValueValidator


class ReviewForm(forms.ModelForm):
    review = forms.Textarea()
    # rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['review']
        widgets = {
          'review': forms.Textarea(attrs={'rows':5}),
          # 'rating': forms.RadioSelect()
        }


