from django import forms
from .models import Recipe, Rating
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'ingredients', 'instructions', 'image']
        labels = {
            'title': 'Recipe Title',
            'category': 'Category',
            'ingredients': 'Ingredients',
            'instructions': 'Instructions',
            'image': 'Upload the image of recipe'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control recipe-input', 'placeholder': 'Enter recipe title'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control recipe-input', 'rows': 5, 'placeholder': 'Enter ingredients, separated by commas'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control recipe-input', 'rows': 8, 'placeholder': 'Enter cooking instructions'})
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control recipe-select'})

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')