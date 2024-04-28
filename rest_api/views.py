from django.shortcuts import render
#importacion de librerias
# Construye el rest
from rest_framework.response import Response
# Visualizacion del API rest
from rest_framework.decorators import api_view
#csrf es un protocolo de seguridad
from django.views.decorators.csrf import csrf_exempt
#le da formato JSON a los serializers
from rest_framework.parsers import JSONParser   
# importa libreria de codigos de respuesta
from rest_framework import status

from aplicacionweb.models import Producto
from .serializers import ProductoSerializer

from aplicacionweb.models import Categoria
from .serializers import CategoriaSerializer

@csrf_exempt
@api_view(['GET', 'POST'])

def lista_Productos(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def lista_Categorias(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategoriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)