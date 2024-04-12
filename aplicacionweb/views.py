from django.shortcuts import render
from .models import Usuario

# Create your views here.
def home(request):
    return render(request, 'aplicacionweb/home.html')

def cooperativo(request):
    return render(request, 'aplicacionweb/cooperativo.html')

def deckbuilding(request):
    return render(request, 'aplicacionweb/deckbuilding.html')

def eurogames(request):
    return render(request, 'aplicacionweb/eurogames.html')

def familiar(request):
    return render(request, 'aplicacionweb/familiar.html')

def solitarios(request):
    return render(request, 'aplicacionweb/solitarios.html')

def iniciarsesion(request):
    return render(request, 'aplicacionweb/iniciarsesion.html')

def registrousuario(request):
    return render(request, 'aplicacionweb/registrousuario.html')

def recuperarcontrasena(request):
    return render(request, 'aplicacionweb/recuperarcontrasena.html')

def editarperfil(request):
    return render(request, 'aplicacionweb/editarperfil.html')

#panel crud
def panel_moderacion(request):
    return render(request, 'aplicacionweb/panel_moderacion.html')

#Metodo para el crud de usuarios (1ra version)
def panel_moderacion(request):
    usuarios = Usuario.objects.all() # SELECT * FROM Usuario
    
    context = {
        'usuarios': usuarios
        }
    
    datos = {'usuarios': usuarios}
    return render(request, 'aplicacionweb/panel_moderacion.html', context)







