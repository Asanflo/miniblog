from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Articles(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    updated_at = models.DateTimeField(auto_now= True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title