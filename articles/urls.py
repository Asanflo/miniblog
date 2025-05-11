from django.urls import path

from .views import listeArticles, ArticlesAPI

urlpatterns = [
    path('listarticles/', listeArticles, name="listarticles"),
    path('articlesapiview/', ArticlesAPI.as_view(), name='Articleslist'),#Url permettant l'execution des actions HTTP GET et POST
    path('articlesapiview/<int:pk>', ArticlesAPI.as_view(), name='Articlesapi'), #Url permettant l'execution du RETRIEVE et PUT
]