from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import permissions

#chargement des models
from .models import Articles
from .forms import ArticlesForm
from .serializers import ArticlesSerializer


# Create your views here.


def listeArticles(request):
    form = ArticlesForm
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarticles")
    articles = Articles.objects.all()
    return render(request, "listArticles.html", {"articles": articles, "form": form})


@api_view(['GET'])
def listapiview(request):
    if request.method == 'GET':
        articles = Articles.objects.all()
        serializer = ArticlesSerializer(articles, many=True).data
    return Response(serializer)


@api_view(['GET'])
def listdetailapi(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    serializer = ArticlesSerializer(article, many=False).data
    return Response(serializer)


class ArticlesAPI(APIView):

    # permission_classes = [DjangoModelPermissions, AllowAny]
    def post(self, request):
        serializer = ArticlesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


