from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_Productos, name='lista_Productos'),
    path('categorias/', views.lista_Categorias, name='lista_Categorias'),
]