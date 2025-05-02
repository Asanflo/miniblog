from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

#chargement des models
from .models import Articles
from .serializers import ArticlesSerializer
# Create your views here.


def listeArticles(request):
    articles = Articles.objects.all()
    return render(request, "listArticles.html", {"articles":articles})

@api_view(['GET'])
def listapiview(request):
    if request.method == 'GET':
        articles = Articles.objects.all()
        serializer = ArticlesSerializer(articles, many=True).data
    return Response(serializer)

@api_view(['GET'])
def listdetailapi(request, pk):
    article = get_object_or_404(Articles,pk=pk)
    serializer = ArticlesSerializer(article, many=False).data
    return Response(serializer)