from django import forms
from django.forms import ModelForm
from .models import Usuario
from .models import Producto

#creamos nuestra clase para el fomrulario desde la base de datos

#UsuarioForm sirve para crear un nuevo usuario (usando el modelo Usuario)
class UsuarioForm(ModelForm):
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'nombreUsuario', 'contrasena', 'direccion']

#ClienteForm sirve para crear un nuevo cliente (usando el modelo Usuario)
class ClienteForm(ModelForm):
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'nombreUsuario', 'contrasena', 'direccion']

#ProductoForm sirve para crear un nuevo producto (usando el modelo Producto)
class ProductoForm(ModelForm):
    
    class Meta:
        model = Producto
        fields = ['nombreProducto', 'precioProducto', 'descripcionProducto', 'imagenProducto', 'categoria', 'proveedor']
        
        