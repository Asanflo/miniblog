from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework import permissions

#chargement des models
from .models import Articles, Userblog, Category, CommentUser
from .forms import ArticlesForm
from .serializers import ArticlesSerializer, UserblogSerializer, CategorySerializer, CommentSerializer


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


class ArticlesAPI(APIView):

    def get_permissions(self):
        if self.request.method == "POST" or self.request.method == "PUT":
            return [IsAuthenticated(), permissions.IsAdminUser()]
        elif self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        else:
            return [AllowAny()]
    def post(self, request):
        serializer = ArticlesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk=None):
        if pk is None:
            articles = Articles.objects.all()
            serializer = ArticlesSerializer(articles, many=True)
            return Response(serializer.data)
        else:
            article = get_object_or_404(Articles, pk=pk)
            serializer = ArticlesSerializer(article, many=False)
            return Response(serializer.data)

    def put(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        serializer = ArticlesSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserBlogViewSet(viewsets.ModelViewSet):
    queryset = Userblog.objects.all()
    serializer_class = UserblogSerializer

    def perform_create(self, serializer):
        serializer.save()

    """def create(self, request, *args, **kwargs):
        # Vérifier si on reçoit une liste (bulk create)
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Comportement normal (création simple)
            return super().create(request, *args, **kwargs)

    def perform_bulk_create(self, serializer):
        serializer.save()"""

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
