import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


def userAvatarContent(instance, filename):
    extension = filename.split('.')[-1]
    username = slugify(instance.user.username)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{username}_{timestamp}.{extension}"
    return os.path.join('avatars',filename)

# Create your models here.
class Userblog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    def __str__(self):
        return self.user.get_full_name()




class Category(models.Model):
    nom = models.CharField(blank=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Articles(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(blank=True)
    updated_at = models.DateTimeField(auto_now= True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(Userblog, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class CommentUser(models.Model):
    content= models.TextField(blank=True)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    author = models.ForeignKey(Userblog, on_delete=models.CASCADE)
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.comment_update == None:
            return f'De {self.author} le {self.comment_created}'
        return f'De {self.author} le {self.comment_update}'