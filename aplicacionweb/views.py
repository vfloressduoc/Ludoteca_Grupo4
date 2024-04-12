from django.shortcuts import render
from .models import Usuario
from .forms import UsuarioForm  # Asegúrate de importar tu formulario


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

#Metodo para listar y ver usuarios
def panel_moderacion(request):
    usuarios = Usuario.objects.all() # SELECT * FROM Usuario
    
    context = {
        'usuarios': usuarios
        }
    
    datos = {'usuarios': usuarios}
    return render(request, 'aplicacionweb/panel_moderacion.html', context)

#form_usuario
# def form_usuario(request):
#     form = UsuarioForm()  # Crea una nueva instancia de tu formulario
#     return render(request, 'aplicacionweb/form_usuario.html', {'form': form}) #El form no esta en la guia lo tuve que agregar para que se vieran los items


def form_usuario(request):
    #el view sera el encargado de entregar el formulario al template
    if request.method == 'POST':
        #con un request rescatamos los datos del formulario
        form = UsuarioForm(request.POST)
        
        #verificamos si el formulario es valido
        if form.is_valid():
            #guardamos el formulario
            form.save()
            datos = {'form': form, 'mensaje': "Usuario guardado exitosamente"}
        else:
            datos = {'form': form}
    else:
        form = UsuarioForm()  # Crea una nueva instancia de tu formulario
        datos = {'form': form}
            
    return render(request, 'aplicacionweb/form_usuario.html', datos)
            
            







