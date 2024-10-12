# models.py

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.TextField()  # Assuming ingredients are stored as a text field
    instructions = models.TextField()  # Assuming instructions are stored as a text field
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = Rating.objects.filter(recipe=self)
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('recipe', 'user')
