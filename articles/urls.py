from django.urls import path

from .views import listeArticles, listapiview, listdetailapi

urlpatterns = [
    path('listarticles/', listeArticles),
    path('articles-list-api/', listapiview),
    path('articles-listapi/<int:pk>/', listdetailapi),
]