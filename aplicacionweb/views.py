from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm  #formulario de usuario
<<<<<<< Updated upstream
=======
from .forms import ClienteForm  #formulario de usuario
#para iniciar sesion
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect

>>>>>>> Stashed changes


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

def form_del_usuario(request):
    return render(request, 'aplicacionweb/form_del_usuario.html')

#Metodo para listar y ver usuarios
@user_passes_test(lambda u: u.is_superuser)
def panel_moderacion(request):
    usuarios = Usuario.objects.all() # SELECT * FROM Usuario
    
    context = {
        'usuarios': usuarios
        }
    
    datos = {'usuarios': usuarios}
    return render(request, 'aplicacionweb/panel_moderacion.html', context)

# def custom_login_required(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect(reverse('iniciarsesion'))
#     return _wrapped_view

#form_usuario
# def form_usuario(request):
#     form = UsuarioForm()  # Crea una nueva instancia de tu formulario
#     return render(request, 'aplicacionweb/form_usuario.html', {'form': form}) #El form no esta en la guia lo tuve que agregar para que se vieran los items


#vista de formulario de usuario para crear un nuevo usuario
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
            

#vista de formulario de usuario para modificar un usuario
def form_mod_usuario(request, id):
#el id es el que se recibe por parametro apra que sepa a quien editar, es el campo del usuario que le vamos a dar, por ejemplo en este caso el correo electronico unico
#buscando los datos en la base de datos
#b buscamos el usuario por el correo
    usuario = Usuario.objects.get(email=id)
    datos = {
         'form' : UsuarioForm(instance=usuario)
     }   
    
    #ahora le entregamos los datos del usuario al formulario
    if request.method=='POST':
        
     #con request recuperamos los datos del formulario y le agregamos el id modificar
     form = UsuarioForm(data=request.POST, instance=usuario)  
     
     #validamos el formulario
     if form.is_valid():
            form.save()
            
            datos['mensaje'] = "Usuario modificado correctamente"
         
    return render(request, 'aplicacionweb/form_mod_usuario.html', datos)

#vista de formulario de usuario para eliminar un usuario
def form_del_usuario(request, id):
    usuario = Usuario.objects.get(email=id)
    usuario.delete()
    
    return redirect(to="panel_moderacion")




<<<<<<< Updated upstream
=======
#Iniciar sesion 
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['contrasena']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales de usuario incorrecto')
            return render(request, 'aplicacionweb/iniciar_sesion.html')
    else:
        return render(request, 'aplicacionweb/iniciar_sesion.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('home')

#Formulario custom para crear usuarios
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
>>>>>>> Stashed changes
