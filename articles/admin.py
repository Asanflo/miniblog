from django.contrib import admin

#Importation des classes du projet
from .models import Articles, Userblog

# Register your models here.
admin.site.register(Articles)
admin.site.register(Userblog)