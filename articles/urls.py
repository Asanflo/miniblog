from django.urls import path, include
from .views import listeArticles, ArticlesAPI, UserViews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViews)

urlpatterns = [
    path('listarticles/', listeArticles, name="listarticles"),
    path('articlesapiview/', ArticlesAPI.as_view(), name='Articleslist'),#Url permettant l'execution des actions HTTP GET et POST
    path('articlesapiview/<int:pk>', ArticlesAPI.as_view(), name='Articlesapi'), #Url permettant l'execution du RETRIEVE et PUT
    path('', include(router.urls)),
]

