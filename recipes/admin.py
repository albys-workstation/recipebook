from django.contrib import admin
from .models import Category, Recipe, Rating

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'average_rating')
    search_fields = ('title', 'author__username', 'category__name')
    list_filter = ('category', 'author')

admin.site.register(Category)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating)
