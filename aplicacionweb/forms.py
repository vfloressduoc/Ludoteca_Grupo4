from django import forms
from django.forms import ModelForm
from .models import Usuario

#creamos nuestra clase para el fomrulario desde la base de datos
class UsuarioForm(ModelForm):
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'nombreUsuario', 'contrasena', 'direccion']
        widgets = {

