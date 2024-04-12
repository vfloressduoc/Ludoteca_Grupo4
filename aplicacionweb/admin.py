from django.contrib import admin

#IMPORTAMOS AL USUARIO
from .models import Usuario

# Register your models here.
admin.site.register(Usuario)