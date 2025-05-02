from django.urls import path

from .views import listeArticles

urlpatterns = [
    path('listarticles/', listeArticles),
]