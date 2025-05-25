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

class UserViews(viewsets.ModelViewSet):
    queryset = Userblog.objects.all()
    serializer_class = UserblogSerializer

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer(instance, data=request.data, partial=partial)
        serializer_class.is_valid(raise_exception=True)
        self.perform_update(serializer_class)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer_class.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
