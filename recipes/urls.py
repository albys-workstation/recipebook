# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import signup
from .views import recipe_list, recipe_detail, recipe_new, recipe_edit, recipe_delete

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/new/', views.recipe_new, name='recipe_new'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('signup/',signup, name='signup'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
