from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Recipe, Category, Rating
from .forms import RecipeForm, RatingForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import logging
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

logger = logging.getLogger(__name__)

def recipe_list(request):
    category_param = request.GET.get('category', None)
    search_query = request.GET.get('search', None)

    logger.debug(f"Category filter: {category_param}")
    logger.debug(f"Search query: {search_query}")

    recipes = Recipe.objects.all()

    if category_param:
        logger.debug(f"Filtering by category: {category_param}")
        recipes = recipes.filter(category__name__iexact=category_param)
    
    if search_query:
        logger.debug(f"Filtering by search query: {search_query}")
        recipes = recipes.filter(title__icontains=search_query)

    logger.debug(f"Number of recipes found: {recipes.count()}")

    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def home(request):
    total_recipes = Recipe.objects.count()
    middle_index = total_recipes // 2
    start_index = max(0, middle_index - 1)  # Start 1 recipe before the middle to get 3
    recipes = Recipe.objects.all()[start_index:start_index + 3]  # Get 3 recipes from the middle

    # Fetch top-rated recipes
    top_rated_recipes = Recipe.objects.annotate(average_rating=Avg('ratings__value')).order_by('-average_rating')[:3]
    
    return render(request, 'recipes/home.html', {'recipes': recipes, 'top_rated_recipes': top_rated_recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                recipe=recipe,
                defaults={'value': form.cleaned_data['value']}
            )
            messages.success(request, 'Your rating has been submitted!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RatingForm()
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'form': form})

@login_required
def recipe_new(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Assign the logged-in user as the author
            recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_new.html', {'form': form})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_edit.html', {'form': form})

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this recipe.")
    
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_delete.html', {'recipe': recipe})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
