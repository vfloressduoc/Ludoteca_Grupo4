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
    avatar = forms.ImageField(required=False)  # Campo para el avatar
    palabra_clave = forms.CharField(required=False)  # Campo para la palabra clave
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'nombreUsuario', 'contrasena', 'direccion', 'avatar', 'palabra_clave']

#ProductoForm sirve para crear un nuevo producto (usando el modelo Producto)
class ProductoForm(ModelForm):
    
    class Meta:
        model = Producto
        fields = ['nombreProducto', 'precioProducto', 'descripcionProducto', 'imagenProducto', 'categoria', 'proveedor']
        

