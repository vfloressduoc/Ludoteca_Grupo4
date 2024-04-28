from rest_framework import serializers
from aplicacionweb.models import Producto, Categoria

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['idProducto', 'nombreProducto', 'precioProducto', 'descripcionProducto', 'imagenProducto', 'categoria', 'proveedor']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre']

