from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm  #formulario de usuario
from .forms import ClienteForm  #formulario de usuario
#para iniciar sesion
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserChangeForm




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
    return render(request, 'aplicacionweb/iniciar_sesion.html')

def registrousuario(request):
    return render(request, 'aplicacionweb/registrousuario.html')

def recuperarcontrasena(request):
    return render(request, 'aplicacionweb/recuperarcontrasena.html')

class EditarPerfilForm(UserChangeForm):
    password = None  # No incluir el campo de contraseña en el formulario

    class Meta:
        model = User
        fields = ('username', 'email', )

def editarperfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'aplicacionweb/editarperfil.html', {'form': form, 'mensaje': 'Perfil actualizado correctamente'})
    else:
        form = EditarPerfilForm(instance=request.user)
        return render(request, 'aplicacionweb/editarperfil.html', {'form': form})

#Metodo para listar y ver usuarios
def panel_moderacion(request):
    usuarios = User.objects.all() # SELECT * FROM auth_user
    
    context = {
        'usuarios': usuarios
    }
    
    return render(request, 'aplicacionweb/panel_moderacion.html', context)

#form_usuario
# def form_usuario(request):
#     form = UsuarioForm()  # Crea una nueva instancia de tu formulario
#     return render(request, 'aplicacionweb/form_usuario.html', {'form': form}) #El form no esta en la guia lo tuve que agregar para que se vieran los items


#vista de formulario de usuario para crear un nuevo usuario (Usando 'User' de Django)
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', )

def form_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            form = CustomUserCreationForm()  # Crea una nueva instancia del formulario
            datos = {'form': form, 'mensaje': "Usuario guardado exitosamente"}
        else:
            datos = {'form': form}
    else:
        form = CustomUserCreationForm()
        datos = {'form': form}
            
    return render(request, 'aplicacionweb/form_usuario.html', datos)
            

#vista de formulario de usuario para modificar un usuario (Usando 'User' de Django)
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_superuser', )

def form_mod_usuario(request, id):
    usuario = User.objects.get(id=id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return render(request, 'aplicacionweb/form_mod_usuario.html', {'form': form, 'mensaje': 'Usuario modificado correctamente'})
    else:
        form = CustomUserChangeForm(instance=usuario)
        return render(request, 'aplicacionweb/form_mod_usuario.html', {'form': form})
    

#vista de formulario de usuario para eliminar un usuario (Usando 'User' de Django)
def form_del_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    
    return redirect(to="panel_moderacion")



#Registro de Cliente (Usando 'User' de Django)
def reg_clientes(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'aplicacionweb/reg_clientes.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'aplicacionweb/reg_clientes.html', {'form': form})

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
            return redirect('iniciar')
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