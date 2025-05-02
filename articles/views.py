from django.shortcuts import render

#chargement des models
from .models import Articles
# Create your views here.


def listeArticles(request):
    articles = Articles.objects.all()
    return render(request, "listArticles.html", {"articles":articles})