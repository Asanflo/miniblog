from django.urls import path

from .views import listeArticles, listapiview, listdetailapi, ArticlesAPI

urlpatterns = [
    path('listarticles/', listeArticles, name="listarticles"),
    path('articles-list-api/', listapiview),
    path('articles-listapi/<int:pk>/', listdetailapi),
    path('articlesapiview/', ArticlesAPI.as_view(), name='Articlesapi'),
]