from django.contrib import admin

#Importation des classes du projetf
from .models import Articles

# Register your models here.
admin.site.register(Articles)